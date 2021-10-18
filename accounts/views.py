from django.shortcuts import render,get_object_or_404,redirect
from .forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.urls  import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from random import randint
from .utils import require
from order.models import Order


# Create your views here.
def dashboard(request, action):
    order = Order.objects.order_by('-status','date') #Oldest pending orders are shown first
    total_staff = User.objects.count()
    pending_order = order.filter(status = "pending")
    completed_order = order.filter(status = "completed")
    if action == "general":
        general = True
        context = context ={"general":general,"order":order,"total_staff":total_staff, "pending_order":pending_order,"completed_order":completed_order}
    elif action == "manager" and require(request,'manager'):
        manager = True     
        context ={"manager":manager,"total_staff":total_staff, "pending_order":pending_order,"completed_order":completed_order}
    
    elif action == "counter" and require(request, 'counter'):
        counter = True
        context = {"counter":counter,"total_staff":total_staff, "pending_order":pending_order,"completed_order":completed_order}

    elif action == "kitchen" and require(request,'kitchen'):
        kitchen = True
        context ={"kitchen":kitchen,"total_staff":total_staff, "pending_order":pending_order,"completed_order":completed_order}
    else:
        error = True
        context = {"error": error}
    return render(request,'dashboard.html',context)




def add_staff(request):
    manager = True
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile_form.save()
            registered = True
            return redirect('dashboard', action='general')
    else:
        profile_form = UserProfileForm()
        user_form = UserForm()
     
    return render(request,'dashboard.html',{'manager':manager,'profile_form':profile_form, 'user_form':user_form})

def login_user(request):
        
    if request.method == 'POST':
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
            # We use request.POST.get('<variable>') as opposed
            # to request.POST['<variable>'], because the
            # request.POST.get('<variable>') returns None if the
            # value does not exist, while request.POST['<variable>']
            # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    action = 'manager'
                else:
                    try:
                        if user.profile.user_type == 'manager':
                            action = 'manager'
                        elif user.profile.user_type == 'counter':
                            action = 'counter'
                        elif user.profile.user_type == 'kitchen':
                            action = 'kitchen'
                        else:
                            pass
                    except:
                        raise ImproperlyConfigured("Create a profile for the user")
                return redirect('dashboard',action=action)
            else:
                return HttpResponse("Your account is disabled.")
        else:
              # Bad login details were provided. So we can't log the user in.
            form_error= "Invalid login details: {0}, {1}".format(username, password)
            return render(request,'login.html',{'form_error':form_error})
                                # The request is not a HTTP POST, so display the login form.
                                # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})    
    
    

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('login'))
