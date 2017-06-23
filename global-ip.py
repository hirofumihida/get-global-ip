#!/usr/bin/env python

import os, requests, subprocess, boto3
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from json import load
from urllib2 import urlopen

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
    #fname = "output.json"
    datalist = [globalip, datetimeip]
    context = {
        'ipdata': datalist
    }
    print render_template('global-ip.json', context)
    #
    #with open(fname, 'w') as f:
    #    ipdata = render_template('global-ip.json', context)
    #    f.write(ipdata)
 
def main():
    create_json()
 
########################################
 
if __name__ == "__main__":
    main()

