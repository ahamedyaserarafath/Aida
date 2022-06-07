import base64
import json
import os
import atom_feeder
from google.cloud import pubsub_v1
import re


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

def get_incident_map(value):
    if re.search('Service outage', value, re.IGNORECASE) or re.search('Service disruption', value, re.IGNORECASE):
        return "RED"
    if re.search('Update', value, re.IGNORECASE):
        return "ORANGE"
    if re.search('Resolved', value, re.IGNORECASE):
        return "GREEN"
    return "GRAY"

# Publishes a message to a Cloud Pub/Sub topic.
def gcp_status(request):
    atom_feeder_url = "https://status.cloud.google.com/en/feed.atom"
    request_json = request.get_json(silent=True)

    if request.args and 'topic' in request.args:
        topic_name = request.args.get('topic')
    else:
        return ('Missing "topic" parameter.', 400)

    print(f'Publishing message to topic {topic_name}')

    feedparser = atom_feeder.AtomFeeder(atom_feeder_url ,app_name = "GCP-")
    incident_list = feedparser.incident_check()
    incident_data_list = []
    if type(incident_list) is list and not incident_list:
        return ('GCP is doing good', 200)
    for incident_dict in incident_list:
        incident_temp = {}
        incident_temp['title'] = incident_dict['title']
        incident_temp['summary'] = incident_dict['summary']
        incident_temp['statuscolor'] = get_incident_map(incident_dict['title'])
        incident_temp['link'] = incident_dict['link']
        incident_data_list.append(incident_temp)
#     message = '''Diagnosis: Diagnosis: Customer's might experience following:

# 1. External HTTP/S Load Balancing, Cloud CDN - config changes will be accepted & fail to propagate
# 2. Cloud Armor rules may also be affected
# 3. Appengine flex customers may see apps fail to deploy
# 4. Traffic Director may see configs fail to propagate
# 5. VM instance group healthchecks & functionality like autoscaling/autohealing may be affected
# Workaround: None at this time.
# '''
#     message_json = json.dumps({
#         'data': {
#             'status' : incident_status,
#             'message': message
#             },
#     })
    message_json = json.dumps(incident_data_list)
    message_bytes = message_json.encode('utf-8')


    topic_name = topic_name.split(",")
    success_topic = []
    failure_topic = []
    for topic_name_temp in topic_name:
        topic_path = publisher.topic_path(PROJECT_ID, topic_name_temp)
        # Publishes a message
        try:
            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()  # Verify the publish succeeded
            print(f"Successfully publlished the message for {topic_name_temp}")
            success_topic.append(topic_name_temp)
        except Exception as e:
            print(f"Failed to publlish the message for {topic_name_temp} : {e} ")
            failure_topic.append(topic_name_temp)
    
    # TODO: For failure topic need to figure out a way of retrying
    # As if we return failure the every topic will be retried 
    # which cause duplicate messages for customer
    if failure_topic:
        print("Alert us")
    return 'Message published.'

