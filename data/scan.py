from collections import defaultdict
import requests
import csv
import time
from datetime import datetime
import ipdb
from decimal import *
import simplejson as json
import json
import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

response = table.scan()
items = response['Count']
print(items)