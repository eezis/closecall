from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404 #, get_list_or_404

from models import Incident
from forms import CreateIncidentForm


from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin, admin_mailer
from django.conf import settings
from django.core.mail import send_mail


user_msg_incident_created = \
"""Thank you for submitting an Incident Report.

Your report will be immediately available to registered users that visit The Close Call Database website
and ride within 60 miles of the Incident's location.

Email notifications, however, will not be sent out immediately. The Incident Report will be reviewed
for content and clarity before the notification is sent. To ensure that the most helpful information
is included, I contact you via email and ask that you clarify portions of the report before it is
released to a wider audience.

Email notifications will be sent when the Incident Report has been accepted.

Thank you,

Ernest
CCDB"""


# class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, SuccessURLMixinUserProfile, CreateView):
class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, CreateView):
    model = Incident
    # position ties to the geoposition application, it displays the map
    # fields = ['position', 'what', 'date', 'time', ]
    form_class = CreateIncidentForm
    success_url = reverse_lazy('users-incident-list')


    def get_initial(self):
        print u"CreateIncidentView.get_initial :: {} {}".format(self.request.user, self.request.user.id)
        return { 'user': self.request.user }

    def form_valid(self, form):
        # set the user so tthat is saved when the form is committed
        form.instance.user = self.request.user
        Incident = form.save(commit=True)

        print u"CreateIncidentView.form_valid :: {}".format(self.request.user)

        msg = "Incident created by " + self.request.user.username
        admin_mailer('CCDB :: Incident Created', msg)

        # now send an email message to the user
        send_mail('Close Call Database', user_msg_incident_created, 'closecalldatabase@gmail.com', [self.request.user.email])

        # for key, value in self.request.POST.iteritems():
        #     print "{} {}".format(key, value)

        return super(CreateIncidentView, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse('users-incident-list')
    #     # return reverse('users-incident-list', kwargs={'user': self.request.user})


class ListIncidentView(LoginRequiredMixin, ListView):
    model = Incident


class DetailIncidentView(LoginRequiredMixin, DetailView):
    model = Incident

class DeleteIncidentView(LoginRequiredMixin, DeleteView):
    model = Incident
    success_url = reverse_lazy('users-incident-list')



class UpdateIncidentView(LoginRequiredMixin, ValidFormMixin, UpdateView):
    # NOTE: this is using incident_form.html, not update_form.html (specify the lattter if need to use it, and update it accordingly.)

    model = Incident
    form_class = CreateIncidentForm
    ''' Update view will use the incident_form.html by default. That will work ONLY if the Submit value on the form
    # is submit. <input type="submit" value="Submit" />,
    # if the value is Save, e.g. <input type="submit" value="Save" /> then it will CREATE A NEW OBJECT RATHER THAN UPDATE IT!
    '''
    # fields = ['position','what', 'date', 'time', 'vehicle_description', 'color', 'make', 'model',
    #     'license_certain', 'license_uncertain', 'id_it_by',]
    success_url = reverse_lazy('users-incident-list')

    def form_valid(self, form):
        print 'Incident has been updated'
        msg = u'Incident UPDATED by {}' + self.request.user.username + '\nCheck to see if it is still in compliance, \
            or if it material and needs a resend!'
        admin_mailer('CCDB :: Incident ** UPDATED **', msg)
        # send_mail('Close Call Database', 'You updated your incident', 'closecalldatabase@gmail.com', [self.request.user.email])
        return super(UpdateIncidentView, self).form_valid(form)


"""
This one is controlled by me, I specifically mask the id because I want this public, but most of them I don't want public so I will pass a proxy value
if I use this feature a lot, then I should make a model and db table (Class PublicLinkProxy) and generic url, then I could update the table on the fly
using the DB.
"""
def show_this_incident(request, ee_fake_key):
    #the key must be 8 characters long, [a-z0-9-] ee-1-173
    # CO-141108-001  -- the incident on Nelson Road with Justin Hoesse
    if settings.DEV_MODE:
        # print 'DEV MODE TRUE'
        linker = {
            'CO-141108-001': 3,
        }
    else:
        linker = {
            'CO-141108-001': 7,
        }
    # print linker[ee_fake_key]
    I = Incident.objects.get(pk=linker[ee_fake_key])
    # print I.license_uncertain
    # print I.what
    return render(request, 'incident/incident.html', {'incident' : I, 'linker_incident_num': ee_fake_key})



def show_this_incident_for_authed_users(request, incident_id):
    #the key must be 8 characters long, [a-z0-9-] ee-1-173
    # CO-141108-001  -- the incident on Nelson Road with Justin Hoesse
    I = Incident.objects.get(id=incident_id)
    # print I.license_uncertain
    # print I.what
    return render(request, 'incident/incident.html', {'incident' : I, 'linker_incident_num': incident_id})


