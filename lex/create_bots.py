import yaml
import boto3
import os
import time
client = boto3.client('lex-models')
for f in os.listdir('bots'):
    config_file = os.path.join('bots', f)
    if not config_file.endswith('yaml') and not config_file.endswith('yml'):
        continue
    with open(config_file, 'r') as stream:
        bots = yaml.load(stream)
    for k in bots.keys():
        if k == 'checksum':
            continue
        bot = bots[k]
        args = {}
        for l in bot.keys():
            args[l] = bots[k][l]
        if 'checksum' in bots and k in bots['checksum']:
            args['checksum'] = bots['checksum'][k]
        print 'Creating bot: {}'.format(bot['name'])
        resp = client.put_bot(**args)
        if 'checksum' not in bots:
            bots['checksum'] = {}
        bots['checksum'][k] = str(resp['checksum'])
        with open(config_file, 'w') as yaml_file:
            yaml_file.write(yaml.dump(bots, default_flow_style=False))
        while resp['status'] == 'BUILDING':
            print 'Bot is building . . .'
            time.sleep(10)
            resp = client.get_bot(name=bot['name'], versionOrAlias='$LATEST')
        print 'Status: {}'.format(resp['status'])

