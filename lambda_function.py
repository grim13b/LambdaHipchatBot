import os
import json
import lib.requests as requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _header(auth_token):
    return {
        u'Content-Type': u'application/json',
        u'Authorization': u'Bearer %s' % auth_token
    }


def _payload(sender, notify, color, message_format, message):
    return json.dumps({
        u'from': sender,
        u'notify': notify,
        u'message_format': message_format,
        u'color': color,
        u'message': message
    })


# SEE: https://www.hipchat.com/docs/apiv2/method/send_room_notification
def lambda_handler(event, context):

    if not os.environ['AUTH_TOKEN'] and \
            not os.environ['SENDER_NAME'] and \
            not os.environ['ROOM_ID']:
        raise Exception('Missing required environment variable')

    logger.debug('Event: ' + str(event))

    if not event['Records'][0]['Sns']['Message']:
        raise Exception('Illegal argument: Records[0].Sns.Message')

    if not event['Records'][0]['Sns']['Subject']:
        raise Exception('Illegal argument: Records[0].Sns.Subject')

    subject = event['Records'][0]['Sns']['Subject']
    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.debug('Message: ' + str(message))

    if message['NewStateValue'] == 'OK':
        notify_color = u'green'
    elif message['NewStateValue'] == 'ALARM':
        notify_color = u'red'
    else:
        notify_color = u'gray'

    message_body = u'<b>%s<b><br>%s<br>%s<br>' % \
                   (subject, message['AlarmDescription'], message['NewStateReason'])

    logger.debug(message_body)

    response = requests.post(
        u'https://api.hipchat.com/v2/room/%s/notification' % os.environ['ROOM_ID'],
        data=_payload(
            sender=os.environ['SENDER_NAME'],
            notify=True,
            color=notify_color,
            message_format=u'html',
            message=message_body),
        headers=_header(os.environ['AUTH_TOKEN']))

    logger.info(u'Response from HipChat:' + str(response))
    return response.status_code

