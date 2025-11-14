{% if cookiecutter.project_type == 'aws-cdk' -%}
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';

export class {{cookiecutter.__package_name | replace('_', '') | title}}Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Example Lambda function using Python runtime
    const exampleFunction = new lambda.Function(this, 'ExampleFunction', {
      runtime: lambda.Runtime.PYTHON_{% if cookiecutter.python_version_min == '3.11' %}3_11{% elif cookiecutter.python_version_min == '3.12' %}3_12{% elif cookiecutter.python_version_min == '3.13' %}3_13{% endif %},
      handler: 'handler.lambda_handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda')),
      description: 'Example Lambda function for {{cookiecutter.__project_name}}',
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        LOG_LEVEL: 'INFO',
      },
    });

    // Example API Gateway REST API
    const api = new apigateway.RestApi(this, 'ExampleApi', {
      restApiName: '{{cookiecutter.__project_name}} API',
      description: 'API Gateway for {{cookiecutter.__project_name}}',
      deployOptions: {
        stageName: 'prod',
        throttlingRateLimit: 100,
        throttlingBurstLimit: 200,
      },
    });

    // Add a Lambda integration to API Gateway
    const lambdaIntegration = new apigateway.LambdaIntegration(exampleFunction);
    const exampleResource = api.root.addResource('example');
    exampleResource.addMethod('GET', lambdaIntegration);

    // Output the API URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
      description: 'API Gateway URL',
    });
  }
}
{%- endif %}
