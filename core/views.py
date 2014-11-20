from django.shortcuts import render
# from incident.models import Incident

def HomeView(request):
    return render(request, 'home.html')
    # if request.user.is_authenticated():
    #     return render(request, 'home.html', {'incidents': Incident.objects.filter(user_id=request.user.id)})
    # else:
    #     return render(request ,'home.html')

