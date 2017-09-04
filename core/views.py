# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time


from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse, reverse_lazy

# to support oauth functionality
import requests
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from users.models import UserProfile
from core.models import UserInput

# to support the custom 400 and 500 handlers (handler500 , handler404)
from django.shortcuts import render_to_response
from django.template import RequestContext

# import logging
# logger = logging.getLogger('closecall')

# from incident.models import Incident

# from registration.views import RegistrationView
# from forms import MyRegistrationForm, EmailRegistrationForm
# from django.contrib.auth import authenticate, login

from incident.models import Incident
from publish.models import InTheNews

from random import randint
from django.db import IntegrityError

P = True


# Printing is controlled via the P flag, pass any IOError exceptions
def safe_print(msg, print_it=True, email_it=False):
    if P and print_it:
        try:
            print msg
        except IOError:
            pass
    if email_it:
        subject = "Cores View: Registration Message"
        send_mail(subject, msg, 'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)


def admin_mailer(subj, msg):
    ts = time.ctime()
    msg + "\n\n" + ts
    # send_mail(subj, msg,'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)
    send_mail(subj, msg, 'closecalldatabase@gmail.com', ['ernest.ezis@gmail.com',], fail_silently=False)


def input_mailer(subj, msg):
    ts = time.ctime()
    msg + "\n\n" + ts
    # send_mail(subj, msg,'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)
    send_mail(subj, msg, 'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com',], fail_silently=False)


def incident_review_mailer(subj, msg):
    ts = time.ctime()
    msg + "\n\n" + ts
    # send_mail(subj, msg,'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)
    send_mail(subj, msg, 'closecalldatabase@gmail.com', ['ernest.ezis@gmail.com', 'closecalldatabase@gmail' ], fail_silently=False)


def send_incident_notification(subj, msg, recipient, htmlmsg=None):
    to = []
    to.append(recipient)
    if htmlmsg != None:
        send_mail(subj, msg, 'closecalldatabase@gmail.com', to, fail_silently=False, html_message=htmlmsg)
    else:
        send_mail(subj, msg, 'closecalldatabase@gmail.com', to, fail_silently=False)


def HomeView(request):
    if request.user.is_authenticated():
        I = Incident.objects.filter(user=request.user)
        N = InTheNews.objects.all().values('title', 'url', 'tldr')[:5]
        try:
            Local_I = request.user.profile.get_user_incidents()
            # Latest_I = Latest Incidents (most recent) -- might want to modify to get the most recent *dangeruous* instances
            Recent_I = Incident.objects.filter(visible=True).order_by('-id')[:10]
            # return render(request, 'home.html', {'incidents': I, 'news_stories': N, 'local_incidents': Local_I, 'recent_incidents': Recent_I})
            # see line 113 as well if you make changes to the response object
            # return render(request, 'home-new-map.html', {'incidents': I, 'news_stories': N, 'local_incidents': Local_I, 'recent_incidents': Recent_I})
            return render(request, 'home.html', {'incidents': I, 'news_stories': N, 'local_incidents': Local_I, 'recent_incidents': Recent_I})
        except AttributeError:
            msg = """
            Last time there was a problem here, registered users were getting redirected to create a user profile. But the real problem
            In [49]: incidents = Incident.objects.all()
            In [54]: for i in incidents:
                print i.position, i.address, i.user

            49.2459762,-123.10122899999999 168 East 28th Avenue, Vancouver, BC V5V 3R1, Canada jwerner
            None  Stephen Banister
            33.8552123,-83.8922349 4098 Bay Creek Road, Loganville, GA 30052, USA John Coyle

            I had to delete the incident. Save the data first.
            """

            the_user = u'The Error effected: {} {} \n'.format(request.user.username, request.user.email)

            new_msg = """
            Was this a recent registration? Does a profile exist for this user? The last time I saw this message,
            it was from TandemRider who had a User and an Active registration, but his profile did not exist.
            Is there some sort of Pilot Error here? Should they be directed to their profile page? \n\n
            """

            msg = the_user + new_msg + msg

            send_mail('YIKES HomeView ERROR', msg,'closecalldatabase@gmail.com', ['ernest.ezis@gmail.com',], fail_silently=False)
            # RelatedObjectDoesNotExist: User has no profile.
            # 1. log this
            # 2. send email
            # 3. redirect to create-user-profile (should send it with a message)
            no_user_profile_msg = "You must create a User Profile in order to proceed."
            messages.add_message(request, messages.INFO, no_user_profile_msg)
            return HttpResponseRedirect('/create-user-profile/')

    else:
        # return render(request, 'home.html')
        return render(request, 'home.html')


def SupportView(request):
    return render(request, 'support-ccdb.html')

CCDB_CLIENT_ID= '3869'
CCDB_REDIRECT_URL = 'http://closecalldatabase.com/strava-registration'
USER_PROFILE_EXISTS = False

def user_profile_exists(user):
    safe_print("Inside user_profile_exists")
    try:
        if user.profile:
            safe_print("User Profile Exists")
            return True
    except:
        safe_print("User Profile does NOT Exist!")
        return False


def get_or_create_a_strava_based_password(athlete_id):
    # throw a little salt onto the password based on the strava's athlete id
    safe_print('generating a strava based password')
    return "!!-stava-cCdB-" + str(athlete_id) + '--2-3-1'


# def login_a_user(request, username, athlete_id):
def login_a_user(request, this_user, athlete_id):
    # ensure we have a valide object and that the account is still active
    safe_print(u"attempting to login {}".format(this_user.username))

    password = get_or_create_a_strava_based_password(athlete_id)

    if this_user is None:
        safe_print("HOUSTON WE HAVE A PROBLEM -- login_a_user should not have gotten a null user! Fix earlier in code.")

    safe_print(u"attempting to authenticate {}".format(this_user.username))
    # the next line throws an exception
    # AttributeError: ‘UserProfile’ object has no attribute ‘username’
    # safe_print(u"Testing to see if this works {}".format(this_user.profile.username))
    # if this_user.username != the_user.profile.username:
    #     msg = "Userpofile.username is {} and User.Username is {}".format(this_user.profile.username, this_user.username)
    #     admin_mailer('Mismatched Usernames', msg)


    # note we are going to cross over, from this_user to user
    # wanted to make the syntactical distinction, even though it was obligatory
    user = authenticate(username=this_user.username, password=password)


    if user is not None:
        # the password verified for the user
        if user.is_active:
            safe_print("User is valid, active and authenticated")
            safe_print(u"going to login {}".format(user.username))
            login(request, user)
            return True
        else:
            safe_print("The password is valid, but the account has been disabled!")
            return False
    else:
        # so what happened here? We just did a "get or create password" because it's a strava user
        # so the User.username doesn't exist? Do I need to pass this_user.profile.username?
        safe_print("The username and password were incorrect.")
        return False



def create_new_user(email, created_username, fname, lname, athlete_id=None):
    safe_print("\nEntering create_new_user \n")
    created_password = get_or_create_a_strava_based_password(athlete_id)
    """ ****************************************************************************************************** """
    """ NOTE WELL: a simple create User and save did not work, I needed to use the "create_user" method of User """
    """ ****************************************************************************************************** """
    # new_user = User(username=created_username, first_name=fname, last_name=lname, email=email, password=created_password)
    try:
        new_user = User.objects.create_user(username=created_username, first_name=fname, last_name=lname, email=email, password=created_password)
        new_user.save()
    except IntegrityError:
        # this means we have an instance where there is already on Sam Thomas, and seccond one is trying to join-probably from Strava
        # let's try to add the athlete_id or a random number
        safe_print(u"INTEGRITY ERROR: Probably two Strava user with same name, {} {}, attempting to fix by generating unique username".format(fname,lname))
        if athlete_id not in [None, '']:
            try:
                created_username = created_username + '-' + athlete_id
            except TypeError:
                admin_mailer('TypeError, cores/views.py', 'The values are: \n'
                    + 'created_username: ' + created_username + '\n athlete_id ' + athlete_id )
        else:
            # I can live with the 1 in 1000 chance we gen a duplicate if the user is not coming from Strava
            created_username = created_username + '-' + str((randint(1,1000)))

        safe_print('created_username is: {}'.format(created_username))
        new_user = User.objects.create_user(username=created_username, first_name=fname, last_name=lname, email=email, password=created_password)
        new_user.save()
    except DataError:
        admin_mailer('UNEXPECTED LOGIN ISSUE', 'Are long emails causing problems? See core.views line ~221. \n'
            + email + '\n' + created_username + '\n' + fname + '\n' + lname + '\n' + athlete_id)

    return new_user




def update_strava_email_if_it_has_changed(TheUser, authing_email):
    if TheUser.email != authing_email:
        # EE 6/20/17 -- I stopped sending the email because this was operating as expected --
        # people change their email, update Strava, then it updates here at CCDB when they log in.
        # ---
        # Notify about this unusual condition
        # s1 = "CONFIRM THIS\n"
        # s2 = 'UserName {} registered with original strava email as {} and has changed it to {}\n'.format(TheUser.username, TheUser.email, authing_email)
        # s3 = 'In the admin, look at the oauth_data field to see the original email address, then confirm with user if you want.'
        # safe_print(s1+s2+s3, True, True)
        # Now update the email
        TheUser.email = authing_email
        TheUser.save()


def existing_strava_user(UserFromDB, authing_email, authing_id):
    #safely try to retrieve the recorded Strava Profile ID
    try:
        safe_print("Checking to see if this is an existing user")
        if UserFromDB.profile.created_with not in [None, '']:
            safe_print("Attemptingt to pull Strava ID")
            # safe_print("User email is {}".format(UserFromDB.email))
            previously_recorded_id = UserFromDB.profile.created_with.split('=')[1]
            safe_print("Existing Strava ID is {}, authing one is {}".format(previously_recorded_id, authing_id))

            # safe_print(previously_recorded_id)
            # safe_print(authing_id)

            # all good to here
            # THIS CODE WAS FAILING WITHOUT THE STRING CAST -- makes sense, JSON Data from strava it's a number
            if str(previously_recorded_id).strip() == str(authing_id).strip():
                safe_print('Strava IDs matched, check for updated email address - TURN ON AFTER DEBUG')
                # update the email on the off chance that the user has updated the email in there strava profile

                update_strava_email_if_it_has_changed(UserFromDB, authing_email)

                return True
            else:
                # if the id's don't match it is not the same user
                safe_print('Registering User has same user name as existing Strava User: {}'.format(UserFromDB.username))
                safe_print('But a different Strave Profile ID.')
                safe_print('Therefore it is a new user to register')
                return False
        else:
            safe_print('\nWas expecting a Strava ID in the created_with field, but didn''t find it!\n', True, True)
            return False
    except:
        # There was an issue retrivieving created with, return false and investigate what happened
        # explanation = 'EXCEPTION RETRIEVING created_with field. This can be normal. For instance there was \
        # an existing Sam Thoams from Strava. A Second one attemtped to register. That would produce a valid user \
        # to pass to this function, but then it would cause an exception '
        safe_print('EXCEPTION RETRIEVING created_with field: This can be normal ', True, True)
        return False



# EE 11.26.15 - this new code replaces the old code I commented out below
"""
if user exists
    and has the same Strava Profile ID
        return the user object
    if different ID
    create a user object and return it
else
    create a user object and return it

caveats: Strava usernames are not unique, user of email and user name is better, but
strava users can change their email. Strava uniqueness is on the athlete_id, but that
is part of the UserProfile. Since this can be called by a returning Strava user that is
simply logging in, we need to check the athlete_id. If it's a match we should check email as
well and update if appropriate
"""
def get_or_create_user(email, created_username, fname, lname, athlete_id=None):
    try:
        user = User.objects.get(username=created_username)
        #  if user is None it should already have excepted and will not run this code
        if existing_strava_user(user, email, athlete_id):
            safe_print("Existing_strava_user returned TRUE")
            return user
        else:
            safe_print("Existing_strava_user returned False, go create new user")
            return create_new_user(email, created_username, fname, lname, athlete_id)

    except User.DoesNotExist:
        safe_print("The user does not exist, going to create User Object".format(created_username))
        return create_new_user(email, created_username, fname, lname, athlete_id)



# def strava_registration(request, strava_token):
def strava_registration(request):

    # the request has some URL Paramaters
    # http://closecalldatabase.com/strava-registration?state=mystate&code=75e251e3ff8fff
    # pluck the code!
    strava_token = request.GET.get('code')

    safe_print("Strava Token: {}".format(strava_token))

    if 'errors' in request.body:
        admin_mailer('TROUBLE - Errors from Strava Response', 'There should be an error value \n\n:'  + request.body)


    if strava_token is None:
        admin_mailer('Strava Regisgration Failure - no token', 'The Strava Token is None!')
        user_msg = """
        <p>There was an error with your attempt to login using your Strava Account. You may have entered an incorrect username and password
        combination. You may simply wish to try again.</p>
        <p>IF YOU DO NOT HAVE A STRAVA ACCOUNT, use the <a href="/accounts/register/">custom registration</a> process to create your account.</p>
        """
        messages.add_message(request, messages.INFO, user_msg)
        # Fix these next lines up, once you know where the "Register via Strava is going to go (maybe login page is best"
        # no_user_profile_msg = "You must create a User Profile in order to proceed."
        # messages.add_message(request, messages.INFO, no_user_profile_msg)
        return HttpResponseRedirect('/smart-500/')



    if strava_token == 'error=access_denied':
        # raise Exception("There was an error in the Strava Authentication Attempt")
        admin_mailer('Strava - Bad Token!', 'The Strava Token came back as error=access_denied. Here is the request.body' + request.body)
        user_msg = """
        <p>There was an error with your attempt to login using your Strava Account. This is a very rare occurrence.
        You may simply wish to try again.</p>
        <p>Or you again or use our<a href="/accounts/register/">custom registration</a> process to create your account.</p>
        """
        messages.add_message(request, messages.INFO, user_msg)
        # Fix these next lines up, once you know where the "Register via Strava is going to go (maybe login page is best"
        # no_user_profile_msg = "You must create a User Profile in order to proceed."
        # messages.add_message(request, messages.INFO, no_user_profile_msg)
        return HttpResponseRedirect('/smart-500/')
    else:
        # the response will look like this (instead of strava-registration this is really strava-token-exchange)
        # http://closecalldatabase.com/strava-registration?state=mystate&code=75e251e3ff8fff

        # The application must now exchange the temporary authorization code for an access token, using its client ID and client secret.

        """
        EXAMPLE SUCCESSFULLY AUTHORIZED HTTP RESPONSE
        HTTP/1.1 302

        Location: http://app.com/exchange?state=mystate&code=75e251e3ff8fff

        THIS IS THE INCOMING
        http://closecalldatabase.com/strava-registration?state=mystate&code=75e251e3ff8fff

        Completing the token exchange
        If the user accepts the request to share access to their Strava data, Strava will redirect back to redirect_uri with the
        authorization code (THAT'S HERE THIS IS THE REDIRECT_URI). The application must now exchange the temporary authorization
        code for an access token, using its client ID and client secret.

        Parameters
        client_id:  integer required
        application’s ID, obtained during registration
        client_secret:  string required
        application’s secret, obtained during registration
        code:   string required
        authorization code
        Returns an access_token and a detailed representation of the current athlete.

        DEFINITION
        POST https://www.strava.com/oauth/token
        EXAMPLE REQUEST
        $ curl -X POST https://www.strava.com/oauth/token \
            -F client_id=5 \
            -F client_secret=7b2946535949ae70f015d696d8ac602830ece412 \
            -F code=75e251e3ff8fff
        """

        # s = 'state=mystate&code=75e251e3ff8fff'
        # c = s.split('&')[1].split('=')[1]
        # print c

        # get the exchange code
        StravasExchangeCode = strava_token
        # set the essentials
        CCDB_CLIENT_SECRET = '4e8fbbe9b63e0b59cec0dcce9d1aabadf94ef039'
        STRAVA_GET_AUTH_URL = 'https://www.strava.com/oauth/token'
        # ready the parameters
        payload = {
            'client_id': CCDB_CLIENT_ID,
            'client_secret': CCDB_CLIENT_SECRET,
            'code': StravasExchangeCode,
        }
        # make the request
        r = requests.post(STRAVA_GET_AUTH_URL, params=payload)
        try:
            if P: print "Trying to complete Token Exchange"
        except IOError:
            pass
        if r.status_code == 200:
            try:
                if P: print 'Token Exchange Completed. Strava sent athlete data.'
            except IOError:
                pass
            # thing are cool, lets get the shit we need from what was passed back, and then redirect to the home view!

            # use the Requests library's built-in JSON decoder ftw
            r.json()

            # Okay, we have the data, wth does it look like? This:
            """
            http://strava.github.io/api/v3/oauth/
            EXAMPLE RESPONSE
            {
              "access_token": "83ebeabdec09f6670863766f792ead24d61fe3f9",
              "athlete": {
                "id": 227615,
                "resource_state": 3,
                "firstname": "John",
                "lastname": "Applestrava",
                "profile_medium": "http://pics.com/227615/medium.jpg",
                "profile": "http://pics.com/227615/large.jpg",
                "city": "San Francisco",
                "state": "California",
                "country": "United States",
                "sex": "M",
                "friend": null,
                "follower": null,
                "premium": true,
                "created_at": "2008-01-01T17:44:00Z",
                "updated_at": "2013-09-04T20:00:50Z",
                "follower_count": 273,
                "friend_count": 19,
                "mutual_friend_count": 0,
                "date_preference": "%m/%d/%Y",
                "measurement_preference": "feet",
                "email": "john@applestrava.com",
                "clubs": [ ],
                "bikes": [ ],
                "shoes": [ ]
              }
            }"""

            oauth_resp = r.json()

            # PRINT STATEMENTS CAUSE ERRORS IF THE TERMINAL IS NOT UP -- NEED TO FIX SEE **** AT BOTTOM OF FILE
            # try:
            #     print "\n"
            #     # print oauth_resp
            #     print "\n"
            # except IOError:
            #     # maybe just write to a file here instead?
            #     admin_mailer('SSH DOWN', 'Fix it dumbass!')
            #     pass


            access_token = oauth_resp['access_token'] # <-- the identifies athlete and application (e.g, Ernest Ezis, CCDB)
            athlete_id = oauth_resp['athlete']['id']
            fname = oauth_resp['athlete']['firstname'][:30]
            lname = oauth_resp['athlete']['lastname'][:30]
            city = oauth_resp['athlete']['city']
            state = oauth_resp['athlete']['state']
            country = oauth_resp['athlete']['country']
            email = oauth_resp['athlete']['email']

            safe_print(u"CURRENT STRAVA REGISTRANT:: {} {} {} {} {} {}".format(fname, lname, city, state, country, email))
            # try:
            #     if P: print u"CURRENT STRAVA REGISTRANT:: {} {} {} {} {} {}".format(fname, lname, city, state, country, email)
            # except IOError:
            #     pass



            # ERROR # 1
            # CURRENT STRAVA REGISTRANT:: Helmet Head ~ youtube.com/misshelmethead Hanover NH United States lilogirl2000@aol.com
            # DataError: value too long for type character varying(30)



            # athlete id will be used to create their passwords (is it long enough?) I could bold "strava-" + athlete-id
            # onto it, making it more secure. I should do that.

            # Had to trim the usernames to 30 (I may need to expand the underlying Djano model! See ERROR #1 above)
            created_username = fname + ' ' + lname
            created_username = created_username[:30]

            # this_user = get_or_create_user(email, created_username, fname, lname, password, athlete_id)
            try:
                if P:
                    print u"{} {}".format(fname, lname)
                    print u"{}".format(email)
                    print u"{}".format(created_username)
                    print athlete_id
            except IOError:
                pass


            # The user may be a new registrant, or a returing user so . . . get_or_create pattern
            this_user = get_or_create_user(email, created_username, fname, lname, athlete_id)

            # might want to replace the code below with an assert statement and fire off an email if it fails
            # try:
            #     print u"this_user test: {} <-- should equal --> {}".format(this_user.username, created_username)
            #     # assert I could use an assert for that print test in production,
            # except IOError:
            #     pass


            safe_print("About to test if User_Profile_Exists -- we have a valid user object, \n but maybe not an existing profile \n Is it a new user or returning?")
            if user_profile_exists(this_user):
                # profile exists, so log them in, redirect to home page
                safe_print("UserProfile exits, so just log this user in!")

                if login_a_user(request, this_user, athlete_id):
                    safe_print("authenticated and logged in, redirected to home page\n")
                    return HttpResponseRedirect('/')
                else:
                    # hmmm, this shouldn't happen, what if it does?

                    """ I could just create a new password? """
                    """ I could look up their current password and use it to try again
                    if they fail 3 times then redirect for help?
                    """
                    # >>> from django.contrib.auth.models import User
                    # >>> u = User.objects.get(username='john')
                    # >>> u.set_password('new password')
                    # >>> u.save()

                    # user_having_trouble = u"{} {} : {} : usnermane={} : Id={}".format(fname, lname, email, created_username, athlete_id)
                    # admin_mailer('UNEXPECTED LOGIN ISSUE', 'See view.core if user_profile_exists login attempt. \n' + user_having_trouble )

                    # see 10:18 am email on 10:39 am, in the closecall gmail account
                    admin_mailer('UNEXPECTED LOGIN ISSUE', 'See core.view if user_profile_exists login attempt. \n' + this_user.username)
                    safe_print("TROUBLE -- the login failed, user redirected to login-help-page")

                    return HttpResponseRedirect('/login-help-page')

            else:
                safe_print("There is no UserProfile, so this should be a first time registrant. Create a profile")
                safe_print(u"Creating UserProfile for {} {}".format(fname, lname))
                up = UserProfile(user=this_user, first=fname, last=lname, city=city, state=state, country=country,
                    created_with="Strava=" + str(athlete_id), oauth_data=oauth_resp)
                up.save()

                safe_print("Attempting login")

                login_a_user(request, this_user, athlete_id)

                # seems like success is assume?

                if city == None:
                    city = "NA"
                if state == None:
                    state = "NA"

                # Prepping for the redirection that should occur on a succesful login
                created_user_profile_msg = "This is your User Profile based on your Strava settings. Please Doublecheck the \
                City and State fields below. If your rides are not based out of " + city + ", " + state +" then please update \
                accordingly. Add a Zip or Postal Code for best results, particularly if you live in a large city or metropolitan area."
                messages.add_message(request, messages.INFO, created_user_profile_msg)

                if city in ['None','']:
                    city = ''
                    messages.add_message(request, messages.INFO, 'Please Update Your CITY.')

                if state in ['None','']:
                    state = ''
                    messages.add_message(request, messages.INFO, 'Please Update Your STATE.')


                return HttpResponseRedirect('/update-user-profile/' + str(this_user.profile.id) + '/')


        else: # status_code was not 200, so the request back to strava failed
            s = "Strava Token Exchange Failed." # + strava_token <-- can't do this it's NoneType
            # raise Exception(s)
            # send_mail('Strave Registration Error', s + "from core.views.strava_registration", 'closecalldatabase@gmail.com',['ernest.ezis@gmail.com',], fail_silently=False)
            admin_mailer('Strava Registration Error', s + "from core.views.strava_registration")

            user_msg = """There was an error with your attempt to authorize your account at Strava. Is it possible that you mistyped your Strava Password? Try again or use our
            <a href="/accounts/register/">custom registration</a> to create your account. """
            messages.add_message(request, messages.INFO, user_msg)

            return HttpResponseRedirect('/accounts/login/')



def redirect_to_strava_login(request):
    # the Strava oauth process kicks off with a redirect to their site, it includes the "client id" for my application
    # and the redirect url -- 'http://closecalldatabase.com/strava-registration' -- which urls.py redirects
    # to the strava_registration view above.

    safe_print("Redirecting to Strava oauth\n")

    return HttpResponseRedirect('https://www.strava.com/oauth/authorize?client_id=' + CCDB_CLIENT_ID +
        '&response_type=code&redirect_uri=' + CCDB_REDIRECT_URL)

def redirect_to_strava_via_login_page(request):
    # this is the login via strava from the login page (should be a returning user - above is *likely* a first time registrant)
    return HttpResponseRedirect('https://www.strava.com/oauth/authorize?client_id=' + CCDB_CLIENT_ID +
        '&response_type=code&redirect_uri=' + CCDB_REDIRECT_URL)




# class MyRegistrationView(RegistrationView):
#     # point to my form, which includes first and last name
#     # form_class = MyRegistrationForm
#     form_class = EmailRegistrationForm

#     def register(self, request, **cleaned_data):


"""
Helper classes for generic forms
from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin
"""

class ValidFormMixin(object):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owned_by = self.request.user
        self.object.save()
        return super(ValidFormMixin, self).form_valid(form)

class FilterToUserMixin(object):
    """
    Ensures that users can only View, Update, Delete the data they create - it is mixed into LoginRequiredMixin below
    """
    def get_queryset(self, *args, **kwargs):
        qs = super(FilterToUserMixin, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)


class LoginRequiredMixin(FilterToUserMixin, object):
    """
    Ensures that user must be authenticated in order to access view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

def show_user_map(request):
    return render(request, 'home-usermap.html')


import logging
logger = logging.getLogger(__name__)

def myfunction():
    logger.debug("this is a debug message!")

def myotherfunction():
    logger.error("this is an error message!!")



# def handler404(request):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


def handler500(request):
    response = render_to_response('smart-500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


def handler404(request):
    response = render_to_response('smart-404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

# def cyrllic_present(msg):
#     a = 'тьдетскийквадроц'
#     print not set(a).isdisjoint(msg)
#     return not set(a).isdisjoint(msg)


def its_spam(msg):
    if '.ru' in msg:
        return True
    if 'SBA lending' in msg:
        return True
    # catch instances that start off like this: https://vk.com/web_16 – РјРµР±РµР
    if msg[0:4].lower() == 'http':
        return True
    # if cyrllic_present(msg):
    #     return True

    userinput = msg.lower()
    spammy = ["cialis", "porn", "viagra", "sex", "casino", u"ส", u"а", u"п", "tiffany outlet", "kate spade",
    "pharma", "forex", "a href", "$", "erotic", "xxx", "naked", "gay", "promote", "fuck", ]
    for i in spammy:
        if i in userinput:
            return True

    return False


class CreateUserInput(CreateView):
    model = UserInput
    template_name = "input/user_input.html"
    success_url = reverse_lazy('thank-you-for-input')

    # define an attribute of the class (this will allow me to pass the parameter in .as_view(subject='Test')
    subject = None

    # fields = ['subject', 'first', 'last', 'email', 'message',]
    fields = ['first', 'last', 'email', 'message', ]

    def get_object(self, queryset=None):
        return queryset.get(subject=self.subject)

    def form_valid(self, form):
        # print self.subject
        # get ip address to see if there the IPs can be blacklisted
        ip = self.request.META.get('REMOTE_ADDR')
        try:
            ip_real =  self.request.META.get('HTTP_X_REAL_IP')
        except:
            pass
        if ip_real == None:
            ip_real = 'HTTP_X_REAL_IP unavailable'

        msg = self.request.POST['message'] + '\n\n' + self.request.POST['email'] + '\n\n' + ip + '\n\n' + ip_real
        if its_spam(msg):
            # print 'Spam!'
            # print self.request.META.get('REMOTE_ADDR')
            # logger.warning("SPAMMER AT ADDRESS: " + self.request.META.get('REMOTE_ADDR'))
            raise PermissionDenied
            # return redirect('http://www.urbandictionary.com/define.php?term=Fuck%20off%20and%20die')

        else:
            form.instance.subject = self.subject
            input_mailer(self.subject, msg)
            return super(CreateUserInput, self).form_valid(form)



    # def form_valid(self, form):
    #     # print self.kwargs.get('slug', None)
    #     print self.slug
    #     # form.instance.subject = subject
    #     # try:
    #     #     print "called"
    #     # except IOError:
    #     #     pass
    #     return super(CreateUserInput, self).form_valid(form)




# ****
"""
Internal Server Error: /strava-registration Traceback (most recent call last):

File "/home/eezis/.virtualenvs/closecall/local/lib/python2.7/site-packages/django/core/handlers/base.py", line 111, in get_response
  response = wrapped_callback(request, *callback_args, **callback_kwargs)
File "/home/eezis/sites/closecall/core/views.py", line 321, in strava_registration
  print "\n"
IOError: [Errno 5] Input/output error

"""