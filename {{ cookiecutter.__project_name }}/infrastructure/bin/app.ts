{% if cookiecutter.project_type == 'aws-cdk' -%}
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { {{cookiecutter.__package_name | replace('_', '') | title}}Stack } from '../lib/stack';

const app = new cdk.App();

new {{cookiecutter.__package_name | replace('_', '') | title}}Stack(app, '{{cookiecutter.__package_name | replace('_', '') | title}}Stack', {
  /* Uncomment to specify AWS Account and Region
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  */

  description: '{{cookiecutter.short_description}}',
});

app.synth();
{%- endif %}
