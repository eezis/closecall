# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
# from django.shortcuts import get_object_or_404 #, get_list_or_404
from django.http import HttpResponseRedirect

from models import Incident
from forms import CreateIncidentForm, AdminScoreForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin, admin_mailer, incident_review_mailer
from django.conf import settings
from django.core.mail import send_mail
from utils import get_youtube_embed_str
from django.contrib.auth.decorators import login_required

user_msg_incident_created = \
"""Thank you for submitting an Incident Report.

[NOTE: I manage this project in my "free time." It may take me up to a week -- sometimes longer if I am travelling -- to process your report.
If you have a submission that demands immediate attention, please email me directly at: ernest.ezis@gmail.com.
Thanks for your patience and understanding.]

Your report will be immediately available to all registered users that visit The Close Call Database website
and will show up under the "Reports in Your Area" tab fo all cyclists that ride within 60 miles of the Incident's location.

Email notifications, however, will not be sent out immediately. The Incident Report will be reviewed
for content and clarity before any email notifications are sent. To ensure that the most helpful information
is included I may contact you via email and ask you to clarify portions of the report before it is
released to a wider audience.

While I understand that every incident is extremely serious when you are on the receiving end, not every submission
will result in an email alert.

If you have a picture or a URL for a video that should be included with your report, simply reply to this email with that information. If you do know how to resize your photos, please do so before sending. A width of about 800px or less is optimal. I will do that if you don't know how.

Thank you,

Ernest Ezis

Close Call Database for Cyclists

"""


# class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, SuccessURLMixinUserProfile, CreateView):
class CreateIncidentView(LoginRequiredMixin, ValidFormMixin, CreateView):
    model = Incident
    # position ties to the geoposition application, it displays the map
    # fields = ['position', 'what', 'date', 'time', ]
    form_class = CreateIncidentForm
    success_url = reverse_lazy('users-incident-list')


    def get_initial(self):
        print "Get Initial"
        try:
            print u"\nCreateIncidentView.get_initial :: {} {}\n".format(self.request.user, self.request.user.id)
        except IOError:
            pass
        return { 'user': self.request.user }

    def form_invalid(self, form):
        print "Form Invalid"
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # print "form_valid"
        # set the user so tthat is saved when the form is committed
        form.instance.user = self.request.user

        if form.instance.youtube_url:
            form.instance.video_embed_string = get_youtube_embed_str(form.instance.youtube_url)      

        Incident = form.save(commit=True)
        try:
            print u"\nCreateIncidentView.form_valid :: {}\n".format(self.request.user)
        except IOError:
            pass

        # EE 11/30/16, I want the ID number on the emails
        try:
            subj = 'CCDB :: Incident ' + str(Incident.pk) + ' Created'
            subj2 = 'Close Call Database -- Report ' + str(Incident.pk)
        except:
            subj = 'CCDB :: Incident Created'
            subj2 = 'Close Call Database'

        msg = "Incident created by " + self.request.user.username + ' :: ' + self.request.user.email
        incident_review_mailer(subj, msg)


        # now send an email message to the user
        send_mail(subj2 , user_msg_incident_created, 'closecalldatabase@gmail.com', [self.request.user.email])

        # for key, value in self.request.POST.iteritems():

        return super(CreateIncidentView, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse('users-incident-list')
    #     # return reverse('users-incident-list', kwargs={'user': self.request.user})


class ListIncidentView(LoginRequiredMixin, ListView):
    model = Incident

    # def get_queryset(self):
    #     qs = super(ListIncidentView, self).get_queryset()
    #     return qs.filter(visible=True)


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
        try:
            print '\n == == == == == == == == == == == == == == == '
            print 'Incident has been updated'
            print ' == == == == == == == == == == == == == == == \n'
        except IOError:
            pass

        # GET THE ID OF THE INCIDENT REPORT THAT IS BEING UPDATED, AND DROP IT INTO THE EMAIL MESSAGE
        the_incident_id = self.request.META.get('HTTP_REFERER', 'ID IS MISSING!')
        # Looks like this -> https://localhost:8000/incident/update/226/

        # swap in
        # the_incident_id = the_incident_id.replace('https://localhost:8000/incident/update','https://closecalldatabase.com/incident/show-detail' )
        the_incident_id = the_incident_id.replace('https://closecalldatabase.com/incident/update','https://closecalldatabase.com/incident/show-detail' )

        msg = u'Incident ' + the_incident_id + ' UPDATED by {}' + self.request.user.username + '\nCheck to see if it is still in compliance, \
            or if it material and needs a resend! Their contact is ' + self.request.user.email
        incident_review_mailer('CCDB :: Incident ** UPDATED **', msg)
        # send_mail('Close Call Database', 'You updated your incident', 'closecalldatabase@gmail.com', [self.request.user.email])
        return super(UpdateIncidentView, self).form_valid(form)


def show_sample_report(request):
    print 'Sample Report Requested from incident.views'
    # enables for unregistered users: https://closecalldatabase.com/incident/show/CO-141108-001/
    I = Incident.objects.get(pk=7)
    return render(request, 'incident/incident_sample_report.html', {'incident' : I, 'linker_incident_num': 7})


"""
This one is controlled by me, I specifically mask the id because I want this public, but most of them I don't want public so I will pass a proxy value
if I use this feature a lot, then I should make a model and db table (Class PublicLinkProxy) and generic url, then I could update the table on the fly
using the DB.
"""
def show_this_incident(request, ee_fake_key):
    #the key must be 8 characters long, [a-z0-9-] ee-1-173
    # CO-141108-001  -- the incident on Nelson Road with Justin Hoesse

    # if settings.DEV_MODE:
    #     # print 'DEV MODE TRUE'
    #     linker = {
    #         'CO-141108-001': 3,
    #         'BIKE-LAW-HELP-1': 3,
    #         'BIKE-LAW-HELP-2': 3,
    #     }
    # else:
    #     linker = {
    #         'CO-141108-001': 7,
    #         'BIKE-LAW-HELP-1': 69,
    #         'BIKE-LAW-HELP-2': 80,
    #     }


    if ee_fake_key.endswith('/'):
        ee_fake_key = ee_fake_key.replace('/','')

    linker = {
        'CO-141108-001': 7,
        'BIKE-LAW-HELP-1': 69,
        'BIKE-LAW-HELP-2': 80,
    }


    print "fake key: {}".format(ee_fake_key)
    print "fake key: {}".format(linker[ee_fake_key])
    I = Incident.objects.get(pk=linker[ee_fake_key])

    return render(request, 'incident/incident.html', {'incident' : I, 'linker_incident_num': ee_fake_key})



def show_this_incident_for_authed_users(request, incident_id):
    #the key must be 8 characters long, [a-z0-9-] ee-1-173

    # 12.3.15 -- I want to make sure that the expiry, set in settings.py, is being set properly
    # so that users do not have to keep logging in
    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
        expires_in_x_seconds = request.session.get_expiry_age()
        days = expires_in_x_seconds / (86400)
        expires_on_date = request.session.get_expiry_date()
        # print
        # print u"USER {} :: EMAIL {} :: Looking at {}".format(username, useremail, incident_id)
        # print "THE SESSION WILL EXPIRE ON: {}  That is {} days".format(expires_on_date, days)
        # print

    try:
        I = Incident.objects.get(id=incident_id)
        if I.visible:
            admin_score_form = AdminScoreForm(initial={'reviewed': I.reviewed, 'accepted': I.accepted, 
                'show_video': I.show_video, 'utility': I.utility, 'utility_comment': I.utility_comment,
                'video_offensive_votes': I.video_offensive_votes, 'ee_show_video': I.ee_show_video, 'visible': I.visible})
            # Thought this would work but TypeError, Object is not iterable
            # admin_score_form = AdminScoreForm(initial=I)
            return render(request, 'incident/incident.html', {'incident' : I, 'linker_incident_num': incident_id, 'admin_score_form': admin_score_form})
        else:
            return render(request, 'incident/notavailable.html')
    except Incident.DoesNotExist:
        return render(request, 'incident/notavailable.html')



def show_all_incidents(request):
    I = Incident.objects.filter(visible=True)
    paginator = Paginator(I, 15) #show do incindents per page

    page = request.GET.get('page')
    try:
        I = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        I = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        I = paginator.page(paginator.num_pages)

    return render(request, 'home-all-incidents.html', {'incidents': I, 'is_paginated': True})

@login_required(login_url='/accounts/login/')
def admin_score(request, pk):
    if request.method == "POST":
        form = AdminScoreForm(request.POST)
        if form.is_valid():
            print "THE SHIZZLE IS VALID"

            I = Incident.objects.get(id=pk)
            I.reviewed = form.cleaned_data['reviewed']
            I.accepted = form.cleaned_data['accepted']
            I.visible = form.cleaned_data['visible']
            I.show_video = form.cleaned_data['show_video']
            I.ee_show_video = form.cleaned_data['ee_show_video']
            I.utility = form.cleaned_data['utility']
            I.utility_comment = form.cleaned_data['utility_comment']
            I.video_offensive_votes = form.cleaned_data['video_offensive_votes']

            I.save()
            redirect_url = '/incident/show-detail/' + str(pk) + '/'
            return redirect(redirect_url)
            # return HttpResponseRedirect('incident/show-detail', incident_id=pk) # Redirect after POST
        else:
            print "THE SHIZZLE IS A GET!!!"
            I = Incident.objects.get(id=pk)
            return redirect('incident/show-detail/' + str(pk) + '/')
            # form = AdminScoreForm()
            # return render(request, 'blog/post_edit.html', {'form': form})




