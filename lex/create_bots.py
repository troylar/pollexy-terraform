#!/usr/bin/python
import yaml
import boto3
import os
import time
from botocore.exceptions import ClientError


class BotManager:
    def __init__(self, **kwargs):
        pass

    def get_alias(self, botName, aliasName):
        try:
            client = boto3.client('lex-models')
            print 'get_alias {}:{}'.format(botName, aliasName)
            resp = client.get_bot_alias(
                name=aliasName,
                botName=botName
            )
            if resp:
                print 'get_alias checksum = {}'.format(resp['checksum'])
                return resp
        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def get_bot(self, **kwargs):
        self.name = kwargs.get('Name')
        self.versionOrAlias = kwargs.get('VersionOrAlias', '$LATEST')
        print 'Getting bot {}:{}'.format(self.name, self.versionOrAlias)
        try:
            client = boto3.client('lex-models')
            resp = client.get_bot(
                name=self.name,
                versionOrAlias=self.versionOrAlias
            )
            if resp:
                print 'get_bot checksum = {}'.format(resp['checksum'])
                return resp
        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def load_bots(self, path):
        bots = {}
        for f in os.listdir(path):
            config_file = os.path.join(path, f)
            print config_file
            if not config_file.endswith('yaml') \
               and not config_file.endswith('yml'):
                continue
            with open(config_file, 'r') as stream:
                bots.update(yaml.load(stream))
            return bots

    def upsert(self, bot):
        args = {}
        for l in bot.keys():
            args[l] = bot[l]
        print 'Creating bot: {}'.format(bot['name'])
        current_bot = self.get_bot(
            Name=bot['name']
        )
        if current_bot:
            args['checksum'] = current_bot['checksum']
        resp = client.put_bot(**args)
        while resp['status'] == 'BUILDING':
            print 'Bot is building . . .'
            time.sleep(10)
            resp = self.get_bot(name=bot['name'])
        print 'Status: {}'.format(resp['status'])
        return bot

    def create_version(self, bot):
        current_bot = self.get_bot(
            Name=bot['name']
        )
        if current_bot:
            bot['checksum'] = current_bot['checksum']
        print 'Creating new version'
        resp = client.create_bot_version(
            name=bot['name'],
            checksum=bot['checksum']
        )
        bot['version'] = str(resp['version'])
        print 'Version = {}'.format(bot['version'])
        return bot

    def update_alias(self, bot, **kwargs):
        alias = kwargs.get('Alias', 'LATEST')
        print 'Updating alias {} for bot {}:{}' \
              .format(alias, bot['name'], bot['version'])
        current_bot = self.get_alias(bot['name'], alias)
        if current_bot:
            print 'Alias exists . . . updating.'
            print 'name={}, version={}, checksum={}' \
                  .format(alias,
                          current_bot['botVersion'],
                          current_bot['checksum'])
            resp = client.put_bot_alias(
                checksum=current_bot['checksum'],
                name=alias,
                botName=current_bot['botName'],
                botVersion=current_bot['botVersion']
            )
        else:
            print 'Alias does NOT exist . . . creating.'
            resp = client.put_bot_alias(
               name=alias,
               botName=current_bot['name'],
               botVersion=current_bot['version']
            )
        print 'Alias updated'


bm = BotManager()
client = boto3.client('lex-models')
bots = bm.load_bots('bots')
for k in bots.keys():
    bot = bots[k]
    bot = bm.upsert(bot)
    bot = bm.create_version(bot)
    bot = bm.update_alias(bot, Version='$LATEST')
