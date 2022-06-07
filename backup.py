import base64
import json
import os

from google.cloud import pubsub_v1


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    print(request_json)
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        pubsub_message = base64.b64decode(request_json['message']['data']).decode('utf-8')
        print(pubsub_message)
        pubsub_message_new = pubsub_message.get_json()
        print(pubsub_message_new['hello'])
        return request_json['message']
    else:
        return f'Hello World!'

# Publishes a message to a Cloud Pub/Sub topic.
def gcp_status(request):
    request_json = request.get_json(silent=True)

    if request.args and 'topic' in request.args:
        topic_name = request.args.get('topic')
    else:
        return ('Missing "topic" parameter.', 400)
    # TODO: Need to add the core logic
    # for now assuming we have a incident on this
    incident = True
    if not incident:
        return ('GCP is doing good', 200)

    print(f'Publishing message to topic {topic_name}')

    
    type(squares) is dict
    incident_status = "Outage"
    message = '''Diagnosis: Diagnosis: Customer's might experience following:

1. External HTTP/S Load Balancing, Cloud CDN - config changes will be accepted & fail to propagate
2. Cloud Armor rules may also be affected
3. Appengine flex customers may see apps fail to deploy
4. Traffic Director may see configs fail to propagate
5. VM instance group healthchecks & functionality like autoscaling/autohealing may be affected
Workaround: None at this time.
'''
    message_json = json.dumps({
        'data': {
            'status' : incident_status,
            'message': message
            },
    })
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
