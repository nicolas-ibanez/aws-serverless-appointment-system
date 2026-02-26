resource "aws_dynamodb_table" "appointments_table" {
    name         = "AppointmentsTable"
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "appointment_id"

    attribute {
        name = "appointment_id"
        type = "S"
    }
    tags = {
        Environment = "dev"
        project     = "ServerlessAppointmentSystem"
    }
    

}