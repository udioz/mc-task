# Cryptocurrency Quotes

The project is divided into three parts: 
### 1. Collector
Collector periodically (every minute) samples an API to get the most recent Cryptocurrency quotes and then save these quotes in a database.

### 2. Ranker
Runs as a result of new quote samples and recalculates quote ranks relative to other markets in the same exchange

### 3. Quoter
An API for developers to get last 24 hour quotes of a pair

# Architecture
To support scalability and simplicity all components were written as an AWS Lambda.
![Architecture](https://drive.google.com/file/d/1pagqS-NCGNU0BVMmuyAf-vU77l9avxYx/view)

The system uses a MySQL database which has 2 tables:
1. quotes - an append only table for storing quote data
```
CREATE TABLE `quotes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `pair` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(35,10) NOT NULL,
  `batch_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `modified_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY (`exchange`),
  KEY (`pair`),
  KEY (`batch_id`),
  KEY (`created_at`),
  KEY (`modified_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```
2. ranks - storing ranks per exchange + pair
```
CREATE TABLE `ranks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `pair` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `the_rank` int DEFAULT NULL,
  `standard_deviation` decimal(35,10) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `modified_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY (`exchange`,`pair`),
  KEY (`exchange`),
  KEY (`pair`),
  KEY (`created_at`),
  KEY (`modified_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```

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

##  Feature request - real time alerts
#### The short version - 
Another lambda that listens to new data and checks if the last quote is greater than 3x last hour average.
I think that if this is the direction we are heading to I would split Ranker to 2 services:
1. Stats - calc stats on data (standard deviation, average, p90, p99 etc.)
2. Ranker - Set a rank to each currency
3. Real time alerts that can check new data against pre computed stats and if it meets a condition like 3x greater than - send an alert (via a notification service)

#### The long version - 
Basically the same only with a more rich featured alerts system where you can define and manage alerts in a more organized way.
