try:
    import unzip_requirements
except ImportError:
    pass
    
import load_languages
import io
import json
from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
import os
import boto3

latest_version = ""
bucket_name = os.getenv('MODEL_BUCKET_NAME', "")
load_resources(u"en")
nlu_engine = SnipsNLUEngine()

def handler(event, context):
    print(event)
    global nlu_engine
    load_latest_model()

    trained_model = nlu_engine.to_byte_array()
    
    if not os.path.exists('/tmp/models'):
        os.makedirs('/tmp/models')
 
    s3 = boto3.client('s3')

    print("uploading training result")
    s3.put_object(Bucket=bucket_name,
        Key="bot/model.json",
        Body=trained_model,
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }
    

def load_latest_model():
    global latest_version
    global bucket_name
    
    if len(bucket_name) > 0:
        client = boto3.client('s3')
        response = client.head_object(Bucket=bucket_name, Key="bot/raw_data.json")
    else:
        raise Exception("Config bucket is undefined")

    load_model()


def load_model():
    global bucket_name
    model_file_path = "/tmp/raw_data.json"

    s3 = boto3.resource('s3')
    
    print("downloading training data to {}".format(model_file_path))
    s3.meta.client.download_file(bucket_name, "bot/raw_data.json", model_file_path)

    train_model(model_file_path)

def train_model(model_file_path):
    global nlu_engine
    print("reading model at {}".format(model_file_path))
    with io.open(model_file_path) as f:
        model = json.load(f)
        nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
        print("training model")
        nlu_engine.fit(model)
