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
    if intent_name == "rds_create_db":
        rds.create_db_instance(
        AllocatedStorage=10,
        DBName="prod",
        DBInstanceIdentifier="NOME_DA_INSTÂNCIA",
        DBInstanceClass="db.t2.micro",
        Engine="mysql",
        MasterUsername="root",
        MasterUserPassword="Sec#atc123",
        Port=3306,
        VpcSecurityGroupIds=["NOME_DO_SECURITY_GROUP"],
    )
        # Chamando Alexa Start
        speech_output = "Tudo bem, vou criar a instância de banco de dados agora mesmo."
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            "Chamando o Serviço RDS", speech_output, "Repromt", should_end_session))
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