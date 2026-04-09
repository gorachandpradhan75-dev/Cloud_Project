from flask import Flask, render_template, request, redirect, send_file
import boto3
import io

app = Flask(__name__)

# AWS S3 connection
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAVZ7QKYAIFMYLOLPA',
    aws_secret_access_key='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',
    region_name='eu-north-1'
)

BUCKET = 'gora-file-app-001'


# Home route (show files)
@app.route('/')
def index():
    files = s3.list_objects_v2(Bucket=BUCKET)
    file_list = []

    if 'Contents' in files:
        for file in files['Contents']:
            file_list.append(file['Key'])

    return render_template('index.html', files=file_list)


# Upload file
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:
        s3.upload_fileobj(
            file,
            BUCKET,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    return redirect('/')


# Delete file
@app.route('/delete/<filename>')
def delete(filename):
    s3.delete_object(Bucket=BUCKET, Key=filename)
    return redirect('/')


# Download file
@app.route('/download/<filename>')
def download(filename):
    file_obj = s3.get_object(Bucket=BUCKET, Key=filename)

    return send_file(
        io.BytesIO(file_obj['Body'].read()),
        download_name=filename,
        as_attachment=True
    )


# Run app (IMPORTANT PART)
if __name__ == '__main__':
    app.run(debug=True)