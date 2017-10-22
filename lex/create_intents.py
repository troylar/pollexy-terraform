import yaml
import boto3
client = boto3.client('lex-models')
with open("intents.yaml", 'r') as stream:
    intents = yaml.load(stream)
for k in intents.keys():
    if k == 'checksum':
        continue
    intent = intents[k]
    args = {}
    for l in intents[k].keys():
        args[l] = intents[k][l]
    if intents.has_key('checksum') and intents['checksum'].has_key(k):
        args['checksum'] = intents['checksum'][k]
    resp = client.put_intent(**args)
    if not intents.has_key('checksum'):
        intents['checksum'] = {}
    intents['checksum'][k] = str(resp['checksum'])
    with open('intents.yaml', 'w') as yaml_file:
        yaml_file.write( yaml.dump(intents, default_flow_style=False))

