# encoding=utf-8

import easywebdav
from ConfigParser import ConfigParser
from datetime import datetime
import json
import os
import requests

config = ConfigParser()
config.read('config.ini')

year = datetime.now().strftime('%Y')

seen = []
if os.path.exists('seen.json'):
    seen = json.load(open('seen.json', 'r'))

webdav = easywebdav.connect(config.get('webdav', 'host'), username=config.get('webdav', 'username'), password=config.get('webdav', 'password'), protocol='https')

for f in webdav.ls(config.get('page', 'path').format(year=year)):
    url = f.name[webdav.baseurl.rfind(':'):]
    if url not in seen and f.contenttype is not None:
        print url
        seen.append(url)
        webdav.download(url, 'temp.json')
        pagecontent = json.load(open('temp.json', 'r'))
        requests.post(
            'https://api.mailgun.net/v2/{}/messages'.format(config.get('mailgun', 'domain')),
            auth=('api', config.get('mailgun', 'key')),
            data={'from': config.get('page', 'sender'),
                  'to': [config.get('page', 'recipient')],
                  'subject': u"[{}] {}".format(config.get('page', 'subject'), pagecontent['properties']['title']),
                  'text': config.get('page', 'body')
                  })

json.dump(seen, open('seen.json', 'w'))
