import os

from flask import Flask, render_template
from humanize import naturalsize

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

MAIN_BUCKET = 'primary-tweets'
SUMMARY_BUCKET = 'primary-tweets-summaries'
CSV_BUCKET = 'primary-tweets-csv'
SUMMARY_CSV_BUCKET = 'primary-tweets-summaries-csv'

################
### OLD AWS CODE

# import boto3
# s3 = boto3.resource('s3')

# def build_objects(bucket):
#     '''Build list of object tuples to render as table.

#        Object structure: (name, url, size)
#     '''
#     objects = []
#     for obj in s3.Bucket(bucket).objects.all():
#         url = s3.meta.client.generate_presigned_url(
#             'get_object', Params={'Bucket': bucket,'Key': obj.key})
#         objects.append((obj.key, url, naturalsize(obj.size)))
#     return objects

################

def build_objects(bucket):
    '''Build list of object tuples to render as table.

       Object structure: (name, url, size)
    '''
    objects = []
    data_dir = 'data/{}'.format(bucket)
    walk_dir = os.path.realpath('..') + '/' + data_dir
    for root, dirs, files in os.walk(walk_dir):
        for file_name in files:
            objects.append((
                file_name,
                data_dir +  '/' + file_name,
                naturalsize(os.path.getsize(walk_dir + '/' + file_name))
                ))
    return objects

@app.route("/")
def index():
    objects = build_objects(MAIN_BUCKET)
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
    app.run(debug=True, host='0.0.0.0')