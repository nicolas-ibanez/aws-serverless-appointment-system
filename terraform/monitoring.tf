# POST
resource "aws_sns_topic" "alarms_topic" {
  name = "appointment-system-alarms"
}

resource "aws_sns_topic_subscription" "email_target" {
  topic_arn = aws_sns_topic.alarms_topic.arn
  protocol  = "email"
  endpoint  = "nicoibanez200@gmail.com"
}

resource "aws_cloudwatch_metric_alarm" "create_lambda_errors" {
  alarm_name          = "CreateAppointmentErrors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60" 
  statistic           = "Sum"
  threshold           = "1"  
  alarm_description   = "Alerta: La Lambda de creación de citas ha fallado."

  dimensions = {
    FunctionName = aws_lambda_function.create_appointment_lambda.function_name
  }

  alarm_actions = [aws_sns_topic.alarms_topic.arn]
}

# GET 
resource "aws_cloudwatch_metric_alarm" "get_lambda_errors" {
  alarm_name          = "GetAppointmentErrors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "Alerta Crítica: La Lambda de lectura (GET) ha fallado."

  dimensions = {
    FunctionName = aws_lambda_function.get_appointment_lambda.function_name
  }

  alarm_actions = [aws_sns_topic.alarms_topic.arn]
}

# PUT
resource "aws_cloudwatch_metric_alarm" "update_lambda_errors" {
  alarm_name          = "UpdateAppointmentErrors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "Alerta Crítica: La Lambda de actualización (PUT) ha fallado."

  dimensions = {
    FunctionName = aws_lambda_function.update_appointment_lambda.function_name
  }

  alarm_actions = [aws_sns_topic.alarms_topic.arn]
}

# DELETE
resource "aws_cloudwatch_metric_alarm" "delete_lambda_errors" {
  alarm_name          = "DeleteAppointmentErrors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "Alerta Crítica: La Lambda de borrado (DELETE) ha fallado."

  dimensions = {
    FunctionName = aws_lambda_function.delete_appointment_lambda.function_name
  }

  alarm_actions = [aws_sns_topic.alarms_topic.arn]
}