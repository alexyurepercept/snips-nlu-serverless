try:
    import unzip_requirements
except ImportError:
    pass

import load_languages
import io
import json
from snips_nlu import load_resources, SnipsNLUEngine
import os
import boto3
 
 
latest_version = ""
bucket_name = os.getenv('MODEL_BUCKET_NAME', "")
load_resources(u"en")
nlu_engine = SnipsNLUEngine()
 
def handler(event, context):
    global nlu_engine
    load_latest_model()
 
    print(event)
    body = json.loads(event.get('body', '{}'))
    response = nlu_engine.parse(body.get('message', ''))
    print(response)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
 
def load_latest_model():
    global latest_version
    global bucket_name
    if len(bucket_name) > 0:
        client = boto3.client('s3')
        response = client.head_object(Bucket=bucket_name, Key="bot/model.json")
 
        print("model version: {}".format(latest_version))
        current_version = response.get('VersionId', response.get("LastModified", "0"))
        if latest_version != current_version:
            latest_version = current_version
            print("not latest version")
    else:
        raise Exception("Config bucket is undefined")
 
    download_model(latest_version)
 
def download_model(model_version):
    global bucket_name
    model_file = "{}.json".format(model_version)
    model_file_path = "/tmp/models/{}".format(model_file)
 
    if not os.path.isfile(model_file_path):
        print("model file doesn't exist, downloading new model to {}".format(model_file_path))
        s3 = boto3.resource('s3')
        if not os.path.exists('/tmp/models'):
            os.makedirs('/tmp/models')
        s3.meta.client.download_file(bucket_name, "bot/model.json", model_file_path)

    load_model(model_file_path)

def load_model(model_file_path):
    global nlu_engine
    print("reading model at {}".format(model_file_path))
    with io.open(model_file_path, 'r+b') as f:
        model = f.read()
        nlu_engine = SnipsNLUEngine.from_byte_array(model)
