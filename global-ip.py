#!/usr/bin/env python

import os, requests, subprocess, boto3, json, time, pytz
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from json import load
from urllib2 import urlopen

ACCESS_ID=os.environ['ACCESS_ID']
ACCESS_KEY=os.environ['ACCESS_KEY']

bucket_name = "hirofumi-globalip"
timestr = time.strftime("%Y%m%d-%H%M%S")

globalip = load(urlopen('http://jsonip.com'))['ip']
jst = pytz.timezone('Asia/Tokyo')
datetimeip = datetime.now(jst)

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def create_json():
    datalist = [globalip, datetimeip]
    context = {
        'ipdata': datalist
    }
    json_key = "global-ip-" + timestr + ".json"
    s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key=ACCESS_KEY)
    obj = s3.Object(bucket_name,json_key)
    test_json = render_template('global-ip.json', context)
    r = obj.put(Body = json.dumps(test_json))
    print render_template('global-ip.json', context)
 
def main():
    create_json()
 
########################################
 
if __name__ == "__main__":
    main()

