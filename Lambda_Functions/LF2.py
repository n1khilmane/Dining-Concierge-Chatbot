
import boto3
import json
import logging
import uuid
import datetime
import logging
import boto3
import json
from botocore.exceptions import ClientError
import requests
import decimal
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



def getSQSMsg():

    
    session = boto3.Session('AKIAZBNUL4HXXUHU5SZD','rb1OGlUiR6qhja4HdImFCoIu5eBiPD+4zm6cSG6Z')
    sqs = session.client("sqs")
    SQS = boto3.client("sqs")

    
    url = 'https://sqs.us-east-1.amazonaws.com/621537911279/DiningChatbot'
    response = SQS.receive_message(
        QueueUrl=url, 
        AttributeNames=['SentTimestamp'],
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    print(response['Messages'][0]['MessageAttributes'])
    print(type(response['Messages'][0]['MessageAttributes']))
    try:
        message = response['Messages'][0]['MessageAttributes']
        if message is None:
            logger.debug("Empty message")
            return None
    except KeyError:
        logger.debug("No message in the queue")
        return None
    message = response['Messages'][0]['MessageAttributes']
    print("Hello")
    SQS.delete_message(
            QueueUrl=url,
            ReceiptHandle=response['Messages'][0]['ReceiptHandle']
            
        )
    logger.debug('Received and deleted message: %s' % response)
    return message

def lambda_handler(event, context):
    
    """
        Query SQS to get the messages
        Store the relevant info, and pass it to the Elastic Search
    """
    
    message = getSQSMsg() 
    if message is None:
        logger.debug("No Cuisine or PhoneNum key found in message")
        return
    cuisine = message["Cuisine"]["StringValue"]
    location = message["Location"]["StringValue"]
    date = message["Date"]["StringValue"]
    time = message["Time"]["StringValue"]
    numOfPeople = message["PeopleCount"]["StringValue"]
    phone_number = message["PhoneNumber"]["StringValue"]
    phone_number = "+1" + phone_number
    if not cuisine or not phone_number:
        logger.debug("No Cuisine or phone number key found in message")
        return
    
    """
        Query database based on elastic search results
        Store the relevant info, create the message and sns the info
    """
    

    es_query = "https://search-cloud9223-v46yxmt7whhfkxkruwlzgnbizu.us-east-1.es.amazonaws.com/_search?q={cuisine}".format(
        cuisine=cuisine)
    master='restaurants'
    passw='Cloud@9223%'
    esResponse = requests.get(es_query,auth=(master,passw))
    print(esResponse)
    data = json.loads(esResponse.content.decode('utf-8'))
    
    try:
        esData = data["hits"]["hits"]
        print(esData)
    except KeyError:
        logger.debug("Error extracting hits from ES response")
    
 
    ids = []
    for restaurants in esData:
        
        ids.append(restaurants['_source']['Restaurant_id'])
        
    
    messageToSend = 'Hello! Here are my {cuisine} restaurant suggestions in {location} for {numPeople} people, for {diningDate} at {diningTime}: '.format(
            cuisine=cuisine,
            location=location,
            numPeople=numOfPeople,
            diningDate=date,
            diningTime=time,
        )

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    itr = 1
    for id in ids:
        if itr == 6:
            break
        response = table.scan(FilterExpression=Attr('id').eq(id))
        item = response['Items'][0]
        if response is None:
            continue
        restaurantMsg = '' + str(itr) + '. '
        name = item['Name']
        address = item['Address']
        restaurantMsg += name +', located at ' + address +'. '
        messageToSend += restaurantMsg
        itr += 1
        
    messageToSend += "Enjoy your meal!!"
    
    try:
        client = boto3.client('sns', region_name= 'us-east-1')
        response = client.publish(
            PhoneNumber=phone_number,
            Message= messageToSend,
            MessageStructure='string'
        )
    except KeyError:
        logger.debug("Error sending ")
    logger.debug("response - %s",json.dumps(response) )
    logger.debug("Message = '%s' PhoneNumber = %s" % (messageToSend, phone_number))
    
    return {
        'statusCode': 200,
        'body': json.dumps("LF2 running succesfully")
    }
    return messageToSend



    
