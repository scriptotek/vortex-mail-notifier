# encoding=utf-8

import easywebdav
from ConfigParser import ConfigParser
from datetime import datetime
import json
import os
import requests
import rollbar

config = ConfigParser()
config.read('config.ini')

rollbar.init(config.get('rollbar', 'token'), 'production')  # access_token, environment

try:
    year = datetime.now().strftime('%Y')

    seen = []
    if os.path.exists('seen.json'):
        seen = json.load(open('seen.json', 'r'))

    webdav = easywebdav.connect(config.get('webdav', 'host'),
                                username=config.get('webdav', 'username'),
                                password=config.get('webdav', 'password'),
                                protocol='https')

    for f in webdav.ls(config.get('page', 'path').format(year=year)):
        url = f.name[webdav.baseurl.rfind(':'):]
        if url not in seen and f.contenttype is not None and url.find('.html') != -1:
            print "New url found: ", url
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

except IOError:
    rollbar.report_message('Got an IOError in the main loop', 'warning')

except:
    # catch-all
    rollbar.report_exc_info()

