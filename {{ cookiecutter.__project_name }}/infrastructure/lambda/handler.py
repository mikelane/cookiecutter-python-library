{% if cookiecutter.project_type == 'aws-cdk' -%}
"""
AWS Lambda handler for {{cookiecutter.__project_name}}.

This is an example Lambda function that can be customized for your use case.
"""
from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Example AWS Lambda handler.

    Args:
        event: Lambda event object containing request data
        context: Lambda context object containing runtime information

    Returns:
        API Gateway response with status code and body
    """
    logger.info('Received event: %s', json.dumps(event))

    try:
        # Example response
        response_body = {
            'message': 'Hello from {{cookiecutter.__project_name}}!',
            'requestId': context.request_id if hasattr(context, 'request_id') else 'local',
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(response_body),
        }
    except Exception as e:  # noqa: BLE001
        logger.exception('Error processing request')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': str(e)}),
        }
{%- endif %}
