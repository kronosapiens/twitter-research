import boto3
from flask import Flask, render_template
from humanize import naturalsize

s3 = boto3.resource('s3')
app = Flask(__name__)

BUCKET = 'primary-tweets'

@app.route("/")
def index():
    objects = []
    for obj in s3.Bucket(BUCKET).objects.all():
        url = s3.meta.client.generate_presigned_url(
            'get_object', Params={'Bucket': BUCKET,'Key': obj.key})
        objects.append((obj.key, url, naturalsize(obj.size)))
    return render_template('index.html', objects=objects)

if __name__ == "__main__":
    app.run(debug=True)