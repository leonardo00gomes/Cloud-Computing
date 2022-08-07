import boto3

def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

# Intent Lambda Alexa
def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    region = 'us-east-1'
    ids = ['id_da_instancia']
    session_attributes = {}
    ec2 = boto3.client('ec2', region_name=region)
    session_attributes = {}
    if intent_name == "terminar":
        ec2.terminate_instances(InstanceIds=ids)
        # Chamando Alexa Start
        speech_output = "Ok, Deixa comigo, vou pedir para excluir a instância neste momento"
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            "Iniciando o Serviço AWS EC2 e excluindo a instância", speech_output, "Repromt", should_end_session))
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