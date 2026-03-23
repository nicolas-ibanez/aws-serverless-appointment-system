resource "aws_api_gateway_rest_api" "api_gateway" {
    name = "appointment-api"
    description = "API for managing appointments"
    api_key_source = "HEADER"
    endpoint_configuration {
        types = ["REGIONAL"]
    }
}

resource "aws_api_gateway_resource" "appointments" {
    parent_id = aws_api_gateway_rest_api.api_gateway.root_resource_id
    rest_api_id = aws_api_gateway_rest_api.api_gateway.id
    path_part = "appointments"
}

resource "aws_api_gateway_resource" "method_id" {
    parent_id = aws_api_gateway_resource.appointments.id
    rest_api_id = aws_api_gateway_rest_api.api_gateway.id
    path_part = "{id}"
}

resource "aws_api_gateway_method" "post_appointment" {
    resource_id   = aws_api_gateway_resource.appointments.id
    rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
    http_method   = "POST"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_integration" {
    rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
    resource_id             = aws_api_gateway_resource.appointments.id
    http_method             = aws_api_gateway_method.post_appointment.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.create_appointment_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_post" {
    statement_id  = "AllowAPIGatewayInvokePOST"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.create_appointment_lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/POST/appointments"
}

resource "aws_api_gateway_method" "get_appointment" {
    rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
    resource_id   = aws_api_gateway_resource.method_id.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_integration" {
    rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
    resource_id             = aws_api_gateway_resource.method_id.id
    http_method             = aws_api_gateway_method.get_appointment.http_method
    integration_http_method = "POST" 
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.get_appointment_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_get" {
    statement_id  = "AllowAPIGatewayInvokeGET"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.get_appointment_lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/GET/appointments/*"
}

resource "aws_api_gateway_method" "update_appointment" {
    rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
    resource_id   = aws_api_gateway_resource.method_id.id
    http_method   = "PUT"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "update_integration" {
    rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
    resource_id             = aws_api_gateway_resource.method_id.id
    http_method             = aws_api_gateway_method.update_appointment.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.update_appointment_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_put" {
    statement_id  = "AllowAPIGatewayInvokePUT"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.update_appointment_lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/PUT/appointments/*"
}

resource "aws_api_gateway_method" "delete_appointment" {
    rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
    resource_id   = aws_api_gateway_resource.method_id.id
    http_method   = "DELETE"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_integration" {
    rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
    resource_id             = aws_api_gateway_resource.method_id.id
    http_method             = aws_api_gateway_method.delete_appointment.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.delete_appointment_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_delete" {
    statement_id  = "AllowAPIGatewayInvokeDELETE"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.delete_appointment_lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/DELETE/appointments/*"
}

resource "aws_api_gateway_deployment" "api_deployment" {
    rest_api_id = aws_api_gateway_rest_api.api_gateway.id

    triggers = {
        redeployment = sha1(jsonencode([
            aws_api_gateway_resource.appointments.id,
            aws_api_gateway_resource.method_id.id,
            aws_api_gateway_method.post_appointment.id,
            aws_api_gateway_integration.post_integration.id,
            aws_api_gateway_method.get_appointment.id,
            aws_api_gateway_integration.get_integration.id,
            aws_api_gateway_method.update_appointment.id,
            aws_api_gateway_integration.update_integration.id,
            aws_api_gateway_method.delete_appointment.id,
            aws_api_gateway_integration.delete_integration.id,
        ]))
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_api_gateway_stage" "api_stage" {
    deployment_id = aws_api_gateway_deployment.api_deployment.id
    rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
    stage_name    = "prod"
}

output "api_url" {
  value = "${aws_api_gateway_stage.api_stage.invoke_url}/appointments"
}