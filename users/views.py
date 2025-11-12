from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView #, DeleteView
# from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from .forms import UserProfileForm
from .models import UserProfile
# from forms import formname
from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin

from django.shortcuts import redirect
from django.contrib import messages

from .forms import UserProfileForm

def CheckForUserProfile(request):
    s = """'Your User Profile is missing. Please complete the form below so that we can provide you with important information
    about any incidences and dangers that occur where you ride.
    """
    messages.info(request, s)
    return redirect('/create-user-profile/')


class CreateUserProfileView(LoginRequiredMixin, ValidFormMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    # position ties to the geoposition application, it displays the map
    # fields = ['first', 'last', 'city', 'state', 'zipcode', 'country', 'email_incidents', ]
    # form_class = CreateIncidentForm
    # success_url = reverse_lazy('home')
    # success_url = reverse_lazy('DetailUserProfileView', kwargs={'userprofile_id': self.id})

    def get_object(self, queryset=None):
        """
        Get existing profile or return None.
        If profile exists (from signal handler), we update it instead of creating new.
        """
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """Override get to handle existing profiles."""
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Override post to handle existing profiles."""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user-profile-detail', kwargs={'pk' : self.object.pk})

    def form_valid(self, form):
        # set the user so that is saved when the form is committed
        form.instance.user = self.request.user

        # Get or create the profile (signal handler may have already created it)
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            # Update existing profile with form data
            for field in form.cleaned_data:
                setattr(profile, field, form.cleaned_data[field])
            profile.save()
            self.object = profile
            print(f"UpdatedUserProfile via CreateView :: {self.request.user} -- {self.request.user.email}")
        except UserProfile.DoesNotExist:
            # Profile doesn't exist, create it
            self.object = form.save(commit=True)
            print(f"CreatedUserProfile :: {self.request.user} -- {self.request.user.email}")

        return redirect(self.get_success_url())


class DetailUserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "users/userprofile_detail.html"
    context_object_name = "userprofile"


class UpdateUserProfileView(LoginRequiredMixin, ValidFormMixin, UpdateView):
    # NOTE: this is using incident_form.html, not update_form.html (specify the lattter if need to use it, and update it accordingly.)

    model = UserProfile
    form_class = UserProfileForm

    # ''' Update view will use the createview_form.html by default. That will work ONLY if the Submit value on the form
    # # is submit. <input type="submit" value="Submit" />,
    # # if the value is Save, e.g. <input type="submit" value="Save" /> then it will CREATE A NEW OBJECT RATHER THAN UPDATE IT!
    # '''
    # fields = ['first', 'last', 'city', 'state', 'country', 'zipcode', 'email_incidents', 'position']
    # success_url = reverse_lazy('home')

    # go back to detail page to confirm
    def get_success_url(self):
        return reverse('user-profile-detail', kwargs={'pk' : self.object.pk})

