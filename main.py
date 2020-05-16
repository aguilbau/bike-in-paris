#!/usr/bin/env python

import datetime
import json
import subprocess
import time
import traceback


# refresh interval in seconds
REFRESH_INTERVAL=60

class Ad:
    type_blacklist = [
        'autre',
        'bmx',
        'appartement',
        'enfant',
        'fixie',
        'piece',
        'pliant',
        'vtt',
        'equipement',
    ]
    size_blacklist = [
        'XL',
        'L',
        'M',
        'XS',
    ]
    keyword_blacklist = [
        'pignon fixe', 'fixie', 'singlespeed', 'single speed', 'monovitesse', 'mono vitesse',
        'pliant', 'pliable',
        'vtt', 'tout terrain',
        '1,80', '1m80',
        '53cm', '54cm', '55cm', '56cm', '57cm', '58cm', '59cm',
        'cadre 53', 'cadre 54', 'cadre 55', 'cadre 56', 'cadre 57', 'cadre 58', 'cadre 59',
        'electrique', 'électrique',
        'enfant', 'fillette',
        'paire',
    ]

    def __init__(self, json):
        self.json = json
        self.parse()

    def get_attribute(self, key):
        for attr in self.json['attributes']:
            if attr['key'] == key:
                return attr['value']
        return None

    def parse(self):
        self.body = self.json['body'].lower()
        self.condition = self.get_attribute('condition')
        self.date = datetime.datetime.strptime(self.json['first_publication_date'], '%Y-%m-%d %H:%M:%S')
        self.has_phone = self.json['has_phone']
        self.images = self.json['images']['urls_large']
        self.owner = self.json['owner']['name']
        self.price = self.json['price'][0]
        self.size = self.get_attribute('bicycle_size')
        self.subject = self.json['subject'].lower()
        self.type = self.get_attribute('bicycle_type')
        self.url = self.json['url']

    def is_interesting(self):
        if self.size in self.size_blacklist:
            return False
        if self.type in self.type_blacklist:
            return False
        for keyword in self.keyword_blacklist:
            if self.subject.find(keyword) != -1:
                return False
            if self.body.find(keyword) != -1:
                return False
        return True

    def __str__(self):
        # we use chr(10), which is a '\n' because format strings
        # can not include backslashes.
        return f'{self.subject} - {self.type} - {self.price}\n' + \
            f'{self.date}\n\n' + \
            f'    {self.body.replace(chr(10), chr(10) + "    ")}\n\n' + \
            f'{self.url}\n' + \
            '---------------------------------------------------------------------'

def get_latest_ad():
    ads = get_latest_ads(only_interesting=False)
    interesting = list(filter(lambda x: x.is_interesting(), ads))
    if len(interesting):
        return interesting[0]
    return ads[0]

def get_latest_ads(newer_than=None, only_interesting=True):
    j = json.loads(subprocess.check_output(['./fetch.sh']))
    ads = map(lambda x: Ad(x), j['data']['ads'])
    if newer_than:
        ads = filter(lambda x: x.date > newer_than.date, ads)
    if only_interesting:
        ads = filter(lambda x: x.is_interesting(), ads)
    return list(ads)

def play_sound(path):
    subprocess.check_output(['mpv', path], stderr=subprocess.STDOUT)

def notify(ads):
    for ad in ads:
        print(ad)
    play_sound('sounds/found.mp3')
    play_sound('sounds/found.mp3')

def main_loop():
    latest = get_latest_ad()
    print(latest)
    while True:
        time.sleep(REFRESH_INTERVAL)
        ads = get_latest_ads(latest)
        if not len(ads):
            continue
        latest = ads[0]
        notify(ads)

def exit_error():
    traceback.print_exc()
    play_sound('sounds/error.mp3')
    exit(1)

def main():
    try:
        main_loop()
    except KeyboardInterrupt:
        exit(0)
    except:
        exit_error()

if __name__ == '__main__':
    main()
