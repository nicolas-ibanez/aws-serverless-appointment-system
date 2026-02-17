# AWS Serverless Appointment System

## The problem

The problem is that small clinics in latin america manage appointments manually via WhatsApp, losing reservations due to the lack of a confirmations system.

## Architecture

The architecture that we use is python and DynamoDB which is non-relational also we need lambda and that is serverless because you dont need a server, aws is in charge its scalability and api gateway which allows using the code or the system using only an url, CloudWatch that logs and monitors of all.

## What works today

Today we have a code of python that interacts with dynamoDB and need to save also today my project connect to dynamoDB and my table then create an unique ID through the time of creation of the appointment, after that use my defined data and finally performs full CRUD operations(Create, read, update, delete) and confirms successful execution.

## What comes next 

I need to adapt the python code for lamda's handler format then integrate the api gateway and CloudWatch and then finally do a real project that resolves the real problem.

## Final goal

The final goal is a complete serverless system that i can defend in english in the correct way for my portafolio and also have the serverless system working and do the certification AWS SAA-C03.