import boto3
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Independent initialization and environment variable usage
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['AppointmentsTable'])

# Strict schema definition to prevent garbage data in DynamoDB
ALLOWED_FIELDS = ['patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'state']

def lambda_handler(event, context):
    try:
        appointment_id = event['pathParameters']['id']
        logger.info("Request received", extra={
            'appointment_id': appointment_id
        })

        body = json.loads(event['body'])

        # Filter only allowed fields from the body
        updates = {k: v for k, v in body.items() if k in ALLOWED_FIELDS}

        logger.info("Fields received vs fields accepted", extra={
            'fields_received': list(body.keys()),
            'fields_accepted': list(updates.keys())
        })
        
        if not updates:
            return {'statusCode': 400, 'body': json.dumps({'message': 'No valid fields provided for update'})}
        
        # Build the DynamoDB UpdateExpression dynamically
        update_expression = 'SET ' + ', '.join([f'#{k} = :{k}' for k in updates])
        expression_names = {f'#{k}': k for k in updates}
        expression_values = {f':{k}': v for k, v in updates.items()}
        
        # Execute the update in DynamoDB
        response = table.update_item(
            Key={'appointment_id': appointment_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
            ConditionExpression="attribute_exists(appointment_id)"
        )

        updated_attributes = response.get('Attributes')

        logger.info("DynamoDB response", extra={
            'appointment_id': appointment_id,
            'attributes_returned': list(updated_attributes.keys()) if updated_attributes else None
        })
        
        return {
            'statusCode': 200, 
            'body': json.dumps({
                'message': 'Appointment updated', 
                'updated_attributes': response.get('Attributes')
            })
        }

    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        logger.warning("Appointment not found", extra={'appointment_id': appointment_id})
        return {'statusCode': 404, 'body': json.dumps({'message': 'Appointment not found'})}   
    except KeyError as e:
        logger.error("Missing path parameter", extra={'error': str(e)})
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing path parameter: id'})}
    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON body'})}
    except Exception as e:
        logger.error("Unexpected error", extra={'error': str(e)}, exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server error'})}