import boto3
from flask import Flask, render_template
from humanize import naturalsize

s3 = boto3.resource('s3')
app = Flask(__name__)

JSON_BUCKET = 'primary-tweets'
SUMMARY_BUCKET = 'primary-tweets-summaries'
CSV_BUCKET = 'primary-tweets-csv'
SUMMARY_CSV_BUCKET = 'primary-tweets-summaries-csv'

def build_objects(bucket):
    objects = []
    for obj in s3.Bucket(bucket).objects.all():
        url = s3.meta.client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket,'Key': obj.key})
        objects.append((obj.key, url, naturalsize(obj.size)))
    return objects

@app.route("/")
def index():
    objects = build_objects(JSON_BUCKET)
    return render_template('index.html', objects=objects)


@app.route("/summaries")
def summaries():
    objects = build_objects(SUMMARY_BUCKET)
    return render_template('index.html', objects=objects)


@app.route("/csv")
def csv():
    objects = build_objects(CSV_BUCKET)
    return render_template('index.html', objects=objects)

@app.route("/summaries_csv")
def summaries_csv():
    objects = build_objects(SUMMARY_CSV_BUCKET)
    return render_template('index.html', objects=objects)

if __name__ == "__main__":
    app.run(debug=True)