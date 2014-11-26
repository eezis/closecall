from django.shortcuts import render
# from incident.models import Incident

# from registration.views import RegistrationView
# from forms import MyRegistrationForm, EmailRegistrationForm
# from django.contrib.auth import authenticate, login


def HomeView(request):
    return render(request, 'home.html')
    # if request.user.is_authenticated():
    #     return render(request, 'home.html', {'incidents': Incident.objects.filter(user_id=request.user.id)})
    # else:
    #     return render(request ,'home.html')


# class MyRegistrationView(RegistrationView):
#     # point to my form, which includes first and last name
#     # form_class = MyRegistrationForm
#     form_class = EmailRegistrationForm

#     def register(self, request, **cleaned_data):
