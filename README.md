# Cryptocurrency Quotes

The project is comprised of 3 parts:

### 1. Collector
The collector periodically (every minute) samples an API to get the most recent Cryptocurrency quotes and then save these quotes in a database.

### 2. Ranker
Runs as a result of new quote samples and recalculates quote ranks relative to other markets in the same exchange

### 3. Quoter
An API for developers to get last 24 hour quotes of a pair

# Architecture
To support scalability and simplicity all components were written as an AWS Lambda.
![Architecture](https://drive.google.com/file/d/1pagqS-NCGNU0BVMmuyAf-vU77l9avxYx/view)

The system uses a MySQL database which has 2 tables:
1. quotes - an append only table for storing quote data
2. ranks - storing ranks per exchange + pair

## Installation
Create the following AWS components:
- VPC - public and private subnets
- Private subnets should use a route table with a NAT gateway
- Security groups so [Lambda can connect to RDS](https://aws.amazon.com/premiumsupport/knowledge-center/connect-lambda-to-an-rds-instance/)
- Lambda for each component
- Lambda layers for dependencies
- For the Quoter lambda create a function URL so it can be invoked via http request
- For Collector lambda create a cloudwatch event that emits every minute
- For Ranker use a SNS or a step machine so once new data is generated Ranker will be invoked

## TODO
- Improve error handling and logging
- Add validation
- Terraform to provision all AWS components
- DB connection pooling
- [Enhance testing](#testing)
- Use ORM to abstract data models
- Address pagination on collector external api call

## Future features
1. configure collector intervals
2. Support more time ranges (not only last24)

## Scaling
- What would you change if you needed to track many metrics?
    * I'd use a message queue to store the results and save to DB in a more controlled pace
    * If needed I'd add a read replica to the DB so the writer node is read free

- What if you needed to sample them more frequently?
    * Same answer as before. We get more data we can simply enqueue it and deal with it "later"
    
- What if you had many users accessing your dashboard to view metrics?
    * if same requests are recurring I can add a cache layer before the DB; If not it will not add any significant value
    * Add a read replica
    * Switch to a distributed no-sql DB such as DynamoDB

## Testing
- add negative scenarios
- add integration tests
- add stress tests
