#!/usr/bin/env python

import os, requests, subprocess, boto3, json, time
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from json import load
from urllib2 import urlopen

bucket_name = "hirofumi-globalip"
timestr = time.strftime("%Y%m%d-%H%M%S")

globalip = load(urlopen('http://jsonip.com'))['ip']
datetimeip = datetime.now()

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
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name,json_key)
    test_json = render_template('global-ip.json', context)
    r = obj.put(Body = json.dumps(test_json))
    #print render_template('global-ip.json', context)
 
def main():
    create_json()
 
########################################
 
if __name__ == "__main__":
    main()

