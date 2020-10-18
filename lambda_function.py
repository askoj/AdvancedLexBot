import json
import boto3
import datetime

def lambda_handler(event, context):
    
    output = "I didn't understand what you said."
    
    intent_name = event['currentIntent']['name'] 
    
    if (intent_name == "AbdulObeid_Hi"):
        output = "Hello from Lambda!"
    
    elif (intent_name == "AbdulObeid_TellDate"):
        output = datetime.date.today().strftime("I'm pretty sure the date is %d / %b / %Y in Northern Virginia at this time.")
    
    elif (intent_name == "AbdulObeid_MixColors"):
        color_mixes = {
                "red_red" : "red",
                "blue_blue" : "blue",
                "yellow_yellow" : "yellow",
                "yellow_blue" : "green",
                "blue_yellow" : "green",
                "yellow_red" : "orange",
                "red_yellow" : "orange",
                "red_blue" : "purple",
                "blue_red" : "purple"
            }
        slot_a = event['currentIntent']['slots']['colorA'].lower().strip()
        slot_b = event['currentIntent']['slots']['colorB'].lower().strip()
        mixed_colors = color_mixes[('%s_%s' % (slot_a, slot_b))]
        output = ("These colors when mixed make the color %s." % (mixed_colors))
        
    elif (intent_name == "AbdulObeid_AddNumbers"):
        
        number_a = int(event['currentIntent']['slots']['numberA'].strip())
        number_b = int(event['currentIntent']['slots']['numberB'].strip())
        output = ("These numbers when added together make %s" % (number_a+number_b))
        
    elif (intent_name == "AbdulObeid_RememberMyName"):
        s3_client = boto3.client('s3')
        bucket_name = 'lexabdulobeid'
        value_name = 'Lex_AbdulObeid_RememberMyName'
        name_to_store = event['inputTranscript'].replace('my name is','').strip()
        s3_client.create_bucket(Bucket=bucket_name)
        response = s3_client.put_object(ACL='public-read',Body=name_to_store,
    		Bucket=bucket_name,ContentEncoding='string',ContentType='text/plain',Key=value_name)
        output = ('I will remember your name, which is %s I believe.' % (name_to_store))
        
    elif (intent_name == "AbdulObeid_ArticulateMyName"):
        s3_client = boto3.client('s3')
        bucket_name = 'lexabdulobeid'
        value_name = 'Lex_AbdulObeid_RememberMyName'
        stored_value = s3_client.get_object(Bucket=bucket_name, Key=value_name)['Body'].read()
        output = 'As I recall, your name is %s' % (stored_value.decode('utf-8'))
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": output
            }
        }
    }