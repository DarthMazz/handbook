```bash
aws cloudformation deploy \
    --template-file my_lambda_template.yaml \
    --stack-name your-lambda-stack \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides SourceCodeBucketName=ma2moto-bucket SourceCodeKey=html_dojo_1.zip
```
