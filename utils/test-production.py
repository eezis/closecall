import sys
# load the project path and virtualenv
sys.path.append("/Users/eae/code/sites/closecall")
sys.path.append("/Users/eae/.virtualenvs/closecall/lib/python2.7/site-packages")

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'closecall.settings'
# import django
# django.setup()

import requests
import re


SITE = 'http://closecalldatabase.com'


def confirm_200(path):
    print 'testing ... {} \t\t'.format(path),
    return requests.get(SITE+path)
    # if r.status_code != 200:
    #     print "ERROR getting " + path
    # else:
    #     return r


def response_contains(huntforthistext, inthispath):
    r = confirm_200(inthispath)

    if r.status_code != 200:
        print "ERROR - status code {}, while fetching {}".format(r.status_code,inthispath)
    else:
        if re.search(huntforthistext, r.text, flags=re.M|re.S|re.I):
            print 'pass'
        else:
            print "ERROR text {} not found in {}".format(huntforthistext, inthispath)


def test_articles():
    # r = confirm_200('/articles/')
    response_contains('An archive of articles and posts', '/articles/')
    response_contains('The law may stipulate', '/articles/cars-turning-left/')
    # test the redirect
    response_contains('The law may stipulate', '/articles/cars-turning-left/https://plus.google.com/share/')


def test_basic_pages():
    response_contains('It sometimes seems like there is little we can do about it.', '/about/')
    response_contains('Everyone thought their specific Incident was isolated', '/faq')
    response_contains('Helpful Resources', '/resources/')



test_articles()
test_basic_pages()