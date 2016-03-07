import boto3
from flask import Flask
from humanize import naturalsize

s3 = boto3.resource('s3')
app = Flask(__name__)

BUCKET = 'primary-tweets'

@app.route("/")
def index():
    page = "ELECTION TWEETS <br>"
    for obj in s3.Bucket(BUCKET).objects.all():
        page += item_line(obj)
    return page

def item_line(obj):
    url = s3.meta.client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET,'Key': obj.key}
        )
    link = '<a href="{}">{}</a>'.format(url, obj.key)
    return '{}: {}<br>'.format(link, naturalsize(obj.size))

if __name__ == "__main__":
    app.run(debug=True)