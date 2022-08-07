import boto3

def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

# Intent Lambda Alexa
def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    region = 'us-east-1'
    session_attributes = {}
    ec2 = boto3.client('ec2', region_name=region)
    session_attributes = {}
    if intent_name == "criar":
        ec2.run_instances(ImageId='TIPO_DE_AMI',MinCount=1,MaxCount=1,InstanceType='t2.micro',KeyName='alexa')
        # Chamando Alexa Start
        speech_output = "Ok, Deixa comigo, vou pedir para criar a imagem linux ubuntu neste momento"
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            "Iniciando criação de Template", speech_output, "Repromt", should_end_session))
    else:
        raise ValueError("Invalid intent")

# Chamada
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': ' - ' + title,
            'content': ' - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }