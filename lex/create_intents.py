import yaml
import boto3
client = boto3.client('lex-models')
with open("intents.yaml", 'r') as stream:
    intents = yaml.load(stream)
for k in intents.keys():
    if k == 'checksum':
        continue
    intent = intents[k]
    if intents.has_key('checksum') and intents['checksum'].has_key(k):
        resp = client.put_intent(
             name=intent['name'],
             description=intent['description'],
             sampleUtterances=intent['sampleUtterances'],
             slots=intent['slots'],
             fulfillmentActivity=intent['fulfillmentActivity'],
             checksum=intents['checksum'][k]
        )
    else:
        resp = client.put_intent(
             name=intent['name'],
             description=intent['description'],
             sampleUtterances=intent['sampleUtterances'],
             fulfillmentActivity=intent['fulfillmentActivity'],
             slots=intent['slots']
        )
    if not intents.has_key('checksum'):
        intents['checksum'] = {}
    intents['checksum'][k] = str(resp['checksum'])
    with open('intents.yaml', 'w') as yaml_file:
        yaml_file.write( yaml.dump(intents, default_flow_style=False))

