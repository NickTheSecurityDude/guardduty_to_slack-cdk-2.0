#######################################################################
# 
# guardduty_to_slack.py
#
# Description:
#  Lambda function, reads the Slack webhook url form the
#  env variable called "URL"
#  Pushes guardduty findings to a slack channel called "#guardduty
#
# Note: This deployment will push findings instantly but there is 
#        about a hour delay in time it takes guardduty to receive
#        the finding
#
#######################################################################

import os
import urllib3
import json
http = urllib3.PoolManager()

def lambda_handler(event, context):
  DEBUG=0

  if DEBUG:
    print(event)

  # Get the slack webhook URL    
  url_= os.environ['URL']

  # Pull the following fields from the guardduty finding    
  account=event['detail']['accountId']
  region=event['detail']['region']
  detail_type=event['detail']['type']
  count=event['detail']['service']['count']
  severity=event['detail']['severity']
  title=event['detail']['title']
  description=event['detail']['description']
  eventFirstSeen=event['detail']['service']['eventFirstSeen']
  eventLastSeen=event['detail']['service']['eventLastSeen']

  # Associate a color and symbol based on the severity of the finding, 
  # ie. red + fire for a severity of 7 or higher
  if severity > 6:
    color="#db1f1f"
    symbol=":fire:"
  elif severity >3:
    color="#faa13c"
    symbol=":warning:"
  else:
    color="#f2c744"
    symbol=":question:"
    
  # Build the message string for slack
  msg_str=symbol+" "+description+"\n"+"Account: "+account+" | Region: "+region+"\n"+"Severity: "+str(severity)+" | Count: "+str(count) \
          +"\nFirstSeen: "+eventFirstSeen+" | LastSeen: "+eventLastSeen
    
  # Build the POST json  
  url = url_
  msg = {
    "channel": "#guardduty",
    "text": "GuardDuty Alert!! "+title,
    "attachments": [{
      "color": color,
      "blocks": [
      {
        "type": "section",
    	"text": {
    	  "type": "mrkdwn",
    	  "text": msg_str
    	}
      }
      ]
    }
    ]
  }

  # Send the message to slack    
  encoded_msg = json.dumps(msg).encode('utf-8')
  resp = http.request('POST',url, body=encoded_msg)

  # Print the result to cloudwatch, ie. 200 OK, 400 error
  print({
    "message": event, 
    "status_code": resp.status, 
    "response": resp.data
  })
