# Snips NLU Serverless

## Overview

This is an bootstrap project demonstrating how to setup Snips NLU into AWS Lambda functions. This serverless project will setup two API endpoints for following tasks

- Model Training
- Model Inference

## Deploy

```
AWS_ACCESS_KEY_ID=<aws_key_id> AWS_SECRET_ACCESS_KEY=<aws_secret_key> deploy --stage <stage> --region ap-southeast-2
```

## Training Dataset

The training dataset file need to be in JSON format, a full documentation on the structure is [here](https://snips-nlu.readthedocs.io/en/latest/dataset.html)

## Training

Need to upload the training dataset to bucket/bot/raw_data.json before triggering the training process. Send GET request to https://apigateway/stage/train to trigger the training process

## Inference

Send POST request to https://apigateway/stage/processIntent with the payload like below to predict the intent

```
{
  "message": "<message>"
}
```
