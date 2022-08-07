import boto3

def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

# Intent Lambda Alexa
def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    session_attributes = {}
    cloudwatch = boto3.client('cloudwatch')
    session_attributes = {}
    if intent_name == "monitorar_memoria":
        cloudwatch.put_metric_alarm(
    AlarmName='Nome_do_alarme',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='Memory',
    Namespace='AWS/EC2',
    Period=60,
    Statistic='Average',
    Threshold=90.0,
    ActionsEnabled=False,
    AlarmDescription='Alarm when server exceeds 90% Memory',
    Dimensions=[
        {
          'Name': 'InstanceId',
          'Value': 'nome_da_instancia'
        },
    ],
    Unit='Seconds'
)
        # Chamando Alexa Start
        speech_output = "Ok, Deixa comigo, vou gerar o alarme no monitoramento de recursos de memória"
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            "Chamando o Serviço Cloudwatch", speech_output, "Repromt", should_end_session))
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