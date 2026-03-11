data "archive_file" "create_appointment_zip" {
    type        = "zip"
    source_file = "../lambdas/create_appointment.py"
    output_path = "${path.module}/createAppointment.zip"
}

data "archive_file" "get_appointment_zip" {
    type        = "zip"
    source_file = "../lambdas/get_appointment.py"
    output_path = "${path.module}/getAppointment.zip"
}

data "archive_file" "update_appointment_zip" {
    type        = "zip"
    source_file = "../lambdas/update_appointment.py"
    output_path = "${path.module}/updateAppointment.zip"
}

data "archive_file" "delete_appointment_zip" {
    type        = "zip"
    source_file = "../lambdas/delete_appointment.py"
    output_path = "${path.module}/deleteAppointment.zip"
}

resource "aws_cloudwatch_log_group" "create_appointment_log" {
  name              = "/aws/lambda/create_appointment" 
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "get_appointment_log" {
  name              = "/aws/lambda/get_appointment" 
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "update_appointment_log" {
  name              = "/aws/lambda/update_appointment" 
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "delete_appointment_log" {
  name              = "/aws/lambda/delete_appointment" 
  retention_in_days = 14
}

resource "aws_lambda_function" "create_appointment_lambda" {
    function_name = "create_appointment"
    role          = aws_iam_role.lambda.arn
    handler       = "create_appointment.lambda_handler"
    runtime       = "python3.9"
    filename      = data.archive_file.create_appointment_zip.output_path 
    source_code_hash = data.archive_file.create_appointment_zip.output_base64sha256
    environment {
        variables = {
            AppointmentsTable = aws_dynamodb_table.appointments_table.name
        }
    }
}

resource "aws_lambda_function" "get_appointment_lambda" {
    function_name = "get_appointment"
    role          = aws_iam_role.lambda.arn
    handler       = "get_appointment.lambda_handler"
    runtime       = "python3.9"
    filename      = data.archive_file.get_appointment_zip.output_path 
    source_code_hash = data.archive_file.get_appointment_zip.output_base64sha256
    environment {
        variables = {
            AppointmentsTable = aws_dynamodb_table.appointments_table.name
        }
    }
  
}

resource "aws_lambda_function" "update_appointment_lambda" {
    function_name = "update_appointment"
    role          = aws_iam_role.lambda.arn
    handler       = "update_appointment.lambda_handler"
    runtime       = "python3.9"
    filename      = data.archive_file.update_appointment_zip.output_path
    source_code_hash = data.archive_file.update_appointment_zip.output_base64sha256
    environment {
        variables = {
            AppointmentsTable = aws_dynamodb_table.appointments_table.name
        }
    }
}

resource "aws_lambda_function" "delete_appointment_lambda" {
    function_name = "delete_appointment"
    role          = aws_iam_role.lambda.arn
    handler       = "delete_appointment.lambda_handler"
    runtime       = "python3.9"
    filename      = data.archive_file.delete_appointment_zip.output_path
    source_code_hash = data.archive_file.delete_appointment_zip.output_base64sha256
    environment {
        variables = {
            AppointmentsTable = aws_dynamodb_table.appointments_table.name
        }
    }
}