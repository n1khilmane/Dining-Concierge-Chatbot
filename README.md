# Dining-Concierge-Chatbot
This application is a serverless, microservice-driven web application built entirely with Amazon Web Services. This chatbot's main function is to make restaurant recommendations to its customers based on their preferences expressed through conversations.

We have support for Yelp-API with suggestions and real time chat. 

## Services Used
1. Amazon S3 - To host the frontend
2. Amazon Lex - To create the bot
3. API Gateway - To set up the API
4. Amazon SQS - to store user requests on a first-come bases
5. ElasticSearch Service - To quickly get restaurant ids based on the user preferences of cuisine collected from SQS
6. DynamoDB - To store the restaurant data collected using Yelp API
7. Amazon SNS - to send restaurant suggestions to users through SMS
8. Lambda - To send data from the frontend to API and API to Lex, validation, collecting restaurant data, sending suggestions using SNS.
9. Yelp API - To get suggestions for food
10. AWS Congito - For authentication
