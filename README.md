# Cryptocurrency Quotes

The project is comprised of 3 parts:

### 1. Collector
The collector periodically (every minute) samples an API to get the most recent Cryptocurrency quotes and then save these quotes in a database.

### 2. Ranker
This component runs as a result of new quote samples and recalculates a quote rank relative to other markets in the exchange

### 3. Quoter
An API for developers to get last 24 hour quotes of a pair

# Architecture
To support scalability and simplicity all components were written as an AWS Lambda.
The system uses a MySQL database which has 2 tables:
1. quotes - an append only table for storing quote data
2. ranks - storing ranks

## Installation
Create the following AWS components:
1. VPC - subnets, route tables, NAT gateway, security groups
2. Lambda for each component
3. Lambda layers for dependencies


Create Lambda layers for requests and mysql-connector-python packages
Create a Lambda function for each component
Upload deployment zip files
Attach layers to each lambda
Add env vars 
https://aws.amazon.com/premiumsupport/knowledge-center/connect-lambda-to-an-rds-instance/



## Future features
1. configure collector intervals
## TODO
Error handling and logging
Validation
Terraform for AWS provisioning
Use env vars
DB connection pooling
Support more time ranges (not only last24)
Use ORM for accessing data models
Address pagination on collector external api call
Leverage AWS Lambda layers to share deps

## Scaling
Use a separate lambda for stdev calcs 

## Question:
Should I focus on one exchange or handle all?
Is SD calc is relative to market in same exchange or all?
I am not sure about naming conventions. var and func names. camel case or snake case?
What should be the rank of a 0 stdev
What is the tests coverage needed for the task considering I am not a python dev

process indexes also not only markets?
