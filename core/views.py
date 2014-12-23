# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
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


# from incident.models import Incident

# from registration.views import RegistrationView
# from forms import MyRegistrationForm, EmailRegistrationForm
# from django.contrib.auth import authenticate, login

from incident.models import Incident
from publish.models import InTheNews


def admin_mailer(subj, msg):
    ts = time.ctime()
    msg + "\n\n" + ts
    # send_mail(subj, msg,'closecalldatabase@gmail.com', ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)
    send_mail(subj, msg,'closecalldatabase@gmail.com', ['ernest.ezis@gmail.com',], fail_silently=False)


def HomeView(request):
    if request.user.is_authenticated():
        I = Incident.objects.filter(user=request.user)
        N = InTheNews.objects.all().values('title','url', 'tldr')[:5]
        # Local_I = Local Incidents
        try:
            Local_I = request.user.profile.get_user_incidents()
            # Latest_I = Latest Incidents (most recent) -- might want to modify to get the most recent *dangeruous* instances
            Recent_I = Incident.objects.all().order_by('-id')[:5]
            return render(request, 'home.html', {'incidents': I, 'news_stories': N, 'local_incidents': Local_I, 'recent_incidents': Recent_I})
        except AttributeError:
            # RelatedObjectDoesNotExist: User has no profile.
            # 1. log this
            # 2. send email
            # 3. redirect to create-user-profile (should send it with a message)
            no_user_profile_msg = "You must create a User Profile in order to proceed."
            messages.add_message(request, messages.INFO, no_user_profile_msg)
            return HttpResponseRedirect('/create-user-profile/')

    else:
        return render(request, 'home.html')


CCDB_CLIENT_ID= '3869'
CCDB_REDIRECT_URL = 'http://closecalldatabase.com/strava-registration'
USER_PROFILE_EXISTS = False

def user_profile_exists(user):
    USER_PROFILE_EXISTS = False
    try :
        user.profile
        try:
            print "user_profile_exists --> user profile does exist"
        except IOError:
            pass
        USER_PROFILE_EXISTS = True
        return True
    except ObjectDoesNotExist:
        try:
            print "user_profile_exists :: checking for UserProfile--> UserProfile does NOT exist"
        except IOError:
            pass
        return False


def get_or_create_a_strava_based_password(athlete_id):
    # throw a little salt onto the password based on the strava's athlete id
    return "!!-stava-cCdB-" + str(athlete_id) + '--2-3-1'


# def login_a_user(request, username, athlete_id):
def login_a_user(request, this_user, athlete_id):
    # ensure we have a valide object and that the account is still active
    try:
        print u"attempting to login {}".format(this_user.username)
    except IOError:
        pass
    password = get_or_create_a_strava_based_password(athlete_id)


    if this_user is None:
        try:
            print "HOUSTON WE HAVE A PROBLEM"
        except IOError:
            pass

    try:
        print u"attempting to authenticate {}".format(this_user.username)
    except IOError:
        pass

    # note we are going to cross over, from this_user to user
    # wanted to make the syntactical distinction, even though it was obligatory
    user = authenticate(username=this_user.username, password=password)

    if user is not None:
        # the password verified for the user
        if user.is_active:
            try:
                print("User is valid, active and authenticated")
                print u"going to login {}".format(user.username)
            except IOError:
                pass
            login(request, user)
            # print "should be logged in \n\n"
            return True
        else:
            try:
                print("The password is valid, but the account has been disabled!")
            except IOError:
                pass
            return False
    else:
        try:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        except IOError:
            pass
        return False


# def get_or_create_user(email, created_username, fname, lname, password, athlete_id):
def get_or_create_user(email, created_username, fname, lname, athlete_id):
    # if user exists
    try:
        # looking up by username and email is stringent but I think I need that
        # user = User.objects.get(username=username, email=email)
        user = User.objects.get(username=created_username)
        try:
            print "the user exists"
        except IOError:
            pass

        if user.email != email:
            old_email = user.email
            # if email on record does not match the current one at strava, swap the current one in and save it
            user.email = email
            user.save()
            # notify me about it, at least for now so I can monitor how this works

            s = 'User: ' + user.username + ' seems to have updated their email address from ' + old_email + ' to ' + email
            #+'. You may wish to confirm that this is what happened to prove that your logic is sound.'

            send_mail('Strava: user changed email?',"from core.views.strava_registration \n\n", 'closecalldatabase@gmail.com',
                ['closecalldatabase@gmail.com', 'ernest.ezis@gmail.com',], fail_silently=False)

        return user

    except User.DoesNotExist:
        try:
            print u"The user does not exist, going to create User: {}".format(created_username)
            # okay, does just the user or just the email exist?
            # what if a user updated their email address at strava?
            print "create a proxy password"
        except IOError:
            pass
        created_password = get_or_create_a_strava_based_password(athlete_id)
        """ ****************************************************************************************************** """
        """ NOTE WELL: a simple create User and save didn ot work, I needed to use the "create_user" method of User """
        """ ****************************************************************************************************** """
        # new_user = User(username=created_username, first_name=fname, last_name=lname, email=email, password=created_password)
        new_user = User.objects.create_user(username=created_username, first_name=fname, last_name=lname, email=email, password=created_password)
        new_user.save()
        return new_user


# def strava_registration(request, strava_token):
def strava_registration(request):

    # the request has some URL Paramaters
    # http://closecalldatabase.com/strava-registration?state=mystate&code=75e251e3ff8fff
    # pluck the code!
    strava_token = request.GET.get('code')

    try:
        print strava_token
    except IOError:
        pass

    if 'errors' in request.body:
        admin_mailer('TROUBLE - Errors from Strava Response', 'There should be an error value \n\n:'  + request.body)


    if strava_token is None:
        admin_mailer('Strava Regisgration Failure', 'The Strava Token is None! ' + request.body)



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
            print "Trying to complete Token Exchange"
        except IOError:
            pass
        if r.status_code == 200:
            try:
                print 'Token Exchange Completed. Strava sent athlete data.'
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
            try:
                print "\n"
                print oauth_resp
                print "\n"
            except IOError:
                # maybe just write to a file here instead?
                admin_mailer('SSH DOWN', 'Fix it dumbass!')
                pass


            access_token = oauth_resp['access_token'] # <-- the identifies athlete and application (e.g, Ernest Ezis, CCDB)
            athlete_id = oauth_resp['athlete']['id']
            fname = oauth_resp['athlete']['firstname'][:30]
            lname = oauth_resp['athlete']['lastname'][:30]
            city = oauth_resp['athlete']['city']
            state = oauth_resp['athlete']['state']
            country = oauth_resp['athlete']['country']
            email = oauth_resp['athlete']['email']
            try:
                print u"CURRENT STRAVA REGISTRANT:: {} {} {} {} {} {}".format(fname, lname, city, state, country, email)
            except IOError:
                pass



            # ERROR # 1
            # CURRENT STRAVA REGISTRANT:: Helmet Head ~ youtube.com/misshelmethead Hanover NH United States lilogirl2000@aol.com
            # DataError: value too long for type character varying(30)



            # athlete id will be used to create their passwords (is it long enough?) I could bold "strava-" + athlete-id
            # onto it, making it more secure. I should do that.

            # Had to trim the usernames to 30 (I may need to expand the underlying Djano model! See ERROR #1 above)
            created_username = fname + ' ' + lname
            created_username = created_username[:30]

            # this_user = get_or_create_user(email, created_username, fname, lname, password, athelete_id)
            try:
                print u"{} {}".format(fname, lname)
                print u"{}".format(email)
                print u"{}".format(created_username)
                print athlete_id
            except IOError:
                pass

            # The user may be a new registrant, or a returing user so . . . get_or_create pattern
            this_user = get_or_create_user(email, created_username, fname, lname, athlete_id)

            try:
                print u"this_user test: {} <-- should equal --> {}".format(this_user.username, created_username)
                # assert I could use an assert for that print test in production,
            except IOError:
                pass


            if user_profile_exists(this_user):
                # profile exists, so log them in, redirect to home page
                try:
                    print "UserProfile exits, so just log this user in!"
                except IOError:
                    pass
                if login_a_user(request, this_user, athlete_id):
                    try:
                        print "authenticated and logged in, redirected to home page\n"
                    except IOError:
                        pass
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
                    admin_mailer('UNEXPECTED LOGIN ISSUE', 'See view.core if user_profile_exists login attempt. \n' + request.body )
                    try:
                        print "TROUBLE -- the login failed, user redirected to login-help-page"
                    except IOError:
                        pass
                    return HttpResponseRedirect('/login-help-page')

            else:
                # There is no UserProfile, so this should be a first time registrant, create a UserProfile
                try:
                    print u"Creating UserProfile for {} {}".format(fname, lname)
                except IOError:
                    pass
                up = UserProfile(user=this_user, first=fname, last=lname, city=city, state=state, country=country,
                    created_with="Strava=" + str(athlete_id), oauth_data=oauth_resp)
                up.save()

                try:
                    print "Attempting login"
                except IOError:
                    pass
                login_a_user(request, this_user, athlete_id)

                # seems like success is assume?

                if city == None:
                    city = "-------"
                if state == None:
                    state = "--"

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
    try:
        print "Redirecting to Strava -- do they signup?\n"
    except IOError:
        admin_mailer('To Strava', 'Did they sign up?')
        pass
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



class CreateUserInput(CreateView):
    model = UserInput
    template_name = "input/user_input.html"
    success_url = reverse_lazy('thank-you-for-input')

    # define an attribute of the class (this will allow me to pass the parameter in .as_view(subject='Test')
    subject = None

    # fields = ['subject', 'first', 'last', 'email', 'message',]
    fields = ['first', 'last', 'email', 'message',]

    def get_object(self, queryset=None):
        return queryset.get(subject=self.subject)

    def form_valid(self, form):
        # print self.subject
        admin_mailer('REQUEST TO WRITE ARTICLE!', self.subject)
        form.instance.subject = self.subject
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