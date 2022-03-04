import pandas
import ipdb
import json
import os


old = pandas.read_csv('/Users/nikhilmane/Desktop/CLOUD/assignment1/data/fin_op2.csv')

new = []
for i in range(len(old)):
	endpoint = 'https://search-cloud9223-v46yxmt7whhfkxkruwlzgnbizu.us-east-1.es.amazonaws.com/restaurant/Restaurant/' + str(i)
	initial = "curl -XPUT -u 'restaurants:Cloud@9223%' 'https://search-cloud9223-v46yxmt7whhfkxkruwlzgnbizu.us-east-1.es.amazonaws.com/restaurantt/_doc/{}' -d ".format(i)
	middle =  "'"+ "{" + '"Restaurant_id": "{}", "Cuisine": "{}"'.format(old['Restaurant_id'][i],old['Cuisine'][i] ) + "}"+"' "
	final =  "-H " + "'" + "Content-Type: application/json" + "'" 
	full = initial + middle + final
	os.system(full)
	#print(full)


