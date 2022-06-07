import base64
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def notify_on_slack(slack_bot_token, channel_id, msg):
    try:
        # Call the chat.postMessage method using the WebClient
        client = WebClient(token=slack_bot_token)
        result = client.chat_postMessage(
            channel=channel_id, 
            text=msg
        )
        return True, ""
    except SlackApiError as e:
        return False, str(e)

def slack_notification(request):
    request_json = request.get_json()
    # customer_channel_ids = List of customer slack channel in comma seperated
    # customer_slack_bot_token = secret token for the slack notification
    if request.args and 'customer_channel_ids' in request.args and 'customer_slack_bot_token' in request.args:
        customer_channel_ids_list = request.args.get('customer_channel_ids').split(",")
        customer_slack_bot_token = request.args.get('customer_slack_bot_token')
    else:
        print ('Missing "customer_channel_ids" parameter and "customer_slack_bot_token" parameter and ')
        return ('Missing "customer_channel_ids" adn "customer_slack_bot_token" parameter.', 400)

    try:
        pubsub_message = json.loads(base64.b64decode(request_json['message']['data']).decode('utf-8'))
    except Exception as e:
        print(f"Failed to get pubsub_message : {e} ")
        return ('Failed to get pubsub_message ', 200)

    for customer_channel_id in customer_channel_ids_list:
        for incident_dict in pubsub_message:
            slack_message_format = "Incident APP : GCP \n" + \
                                     "\nIncident Title : " + incident_dict["title"] + \
                                     "\nIncident Message : " + incident_dict["summary"] + \
                                     "\nIncident Link : " + incident_dict["link"] 
            result, message =  notify_on_slack(customer_slack_bot_token, customer_channel_id, slack_message_format)
            if not result:
                print(f"Error posting slack message: {message}")
    return ('End of Slack notification ', 200)
        


