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
    if 'checksum' in intents and k in intents['checksum']:
        args['checksum'] = intents['checksum'][k]
    resp = client.put_intent(**args)
    if 'checksum' not in intents:
        intents['checksum'] = {}
    intents['checksum'][k] = str(resp['checksum'])
    with open('intents.yaml', 'w') as yaml_file:
        yaml_file.write(yaml.dump(intents, default_flow_style=False))
