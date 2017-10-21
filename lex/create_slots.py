import yaml
import boto3
client = boto3.client('lex-models')
with open("slots.yaml", 'r') as stream:
    slots = yaml.load(stream)
for k in slots.keys():
    if k == 'checksum':
        continue
    if slots.has_key('checksum') and slots['checksum'].has_key(k):
        resp = client.put_slot_type(name=k, enumerationValues=slots[k],
                checksum=slots['checksum'][k])
    else:
        resp = client.put_slot_type(name=k, enumerationValues=slots[k])
    print resp
    if not slots.has_key('checksum'):
        slots['checksum'] = {}
    slots['checksum'][k] = str(resp['checksum'])
    with open('slots.yaml', 'w') as yaml_file:
        yaml_file.write( yaml.dump(slots, default_flow_style=False))

