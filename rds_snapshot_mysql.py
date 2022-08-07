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
    rds = boto3.client('rds', region_name=region)
    session_attributes = {}
    if intent_name == "rds_create_snapshot":
        rds.create_db_snapshot(DBSnapshotIdentifier='nome_do_snapshot', DBInstanceIdentifier='nome_da_instancia')
        # Chamando Alexa Start
        speech_output = "Ok, Deixa comigo, vamos criar um snapshot do ambiente solicitado."
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            "Chamando o Serviço RDS e criando o Snapshot.", speech_output, "Repromt", should_end_session))
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