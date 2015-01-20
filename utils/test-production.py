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
    response_contains('Drivers that are hostile to cyclists', '/')
    response_contains('Safety Related Cycling News', '/news/')
    response_contains('Please Create Your Account', '/accounts/register/')
    response_contains('If you have a Strava account', '/accounts/login/')


def check_for(thistext, inthisresponse):
    if re.search(thistext, inthisresponse, flags=re.M|re.S|re.I):
        print 'pass'
    else:
        print "ERROR text {} not found".format(thistext)


def test_authenticated():
    # logout just to be sure
    r = requests.get('http://closecalldatabase.com/accounts/logout/')

    # now get the CSRF token
    # <input type='hidden' name='csrfmiddlewaretoken' value='xvzoCBSOM7Vecop2pvN6Kx7cs5OiYU2L' />
    r =requests.get('http://closecalldatabase.com/accounts/login/')
    thetoken = re.search("<input type='hidden' name='csrfmiddlewaretoken' value='.*?' />", r.text).group(0)
    # replace everything that isn't the token, so that we are left with the token
    thetoken = re.sub("<input type='hidden' name='csrfmiddlewaretoken' value='", '', thetoken)
    thetoken = re.sub("' />", '', thetoken)

    # print r.text
    print
    print "CSRF token :: {}".format(thetoken)
    print

    # Fill in your details here to be posted to the login form.
    # look at the HTML to see the "name" field for the inputs
    payload = {
        'username': 'eae-test-user',
        'password': '5101-cc-db-!!!-777',
        'csrfmiddlewaretoken': thetoken,
    }


    # get the cookies from the prior request, you have to send the cookies with the session request
    cookies = dict(r.cookies)

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        r = s.post('http://closecalldatabase.com/accounts/login/', data=payload, cookies=cookies)
        # print the html returned or something more intelligent to see if it's a successful login page.
        # print r.text

        cookies = dict(r.cookies)
        # An authorised request.
        r = s.get('http://closecalldatabase.com/', cookies=cookies)
        # print r.text
        check_for('Incidents Reported In Your Area', r.text)


test_articles()
test_basic_pages()
test_authenticated()



