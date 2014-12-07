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

from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin


# class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, SuccessURLMixinUserProfile, CreateView):
class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, CreateView):
    model = Incident
    # position ties to the geoposition application, it displays the map
    # fields = ['position', 'what', 'date', 'time', ]
    form_class = CreateIncidentForm
    success_url = reverse_lazy('users-incident-list')


    def get_initial(self):
        print "CreateIncidentView.get_initial :: {} {}".format(self.request.user, self.request.user.id)
        return { 'user': self.request.user }

    def form_valid(self, form):
        # set the user so tthat is saved when the form is committed
        form.instance.user = self.request.user
        Incident = form.save(commit=True)
        print "CreateIncidentView.form_valid :: {}".format(self.request.user)

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


"""
This one is controlled by me, I specifically mask the id because I want this public, but most of them I don't want public so I will pass a proxy value
if I use this feature a lot, then I should make a model and db table (Class PublicLinkProxy) and generic url, then I could update the table on the fly
using the DB.
"""
def show_this_incident(request, ee_fake_key):
    #the key must be 8 characters long, [a-z0-9-] ee-1-173
    linker = {
        'ee-1-173': 7,
    }
    # print linker[ee_fake_key]
    I = Incident.objects.get(pk=linker[ee_fake_key])
    # print I.what
    return render(request, 'incident/incident.html', {'incident' : I})





