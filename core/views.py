from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# from incident.models import Incident

# from registration.views import RegistrationView
# from forms import MyRegistrationForm, EmailRegistrationForm
# from django.contrib.auth import authenticate, login

from incident.models import Incident
from publish.models import InTheNews

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


