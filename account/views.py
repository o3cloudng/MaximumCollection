from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, ProfileForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from account.models import User, Sector
from django.contrib import messages


# @login_required
def userlogin_old(request):
    from django.contrib.auth import login, authenticate  # add to imports

def userlogin(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.email}! You have been logged in'
                messages.success(request, "You have successfully logged in.")
                return redirect("dashboard")
            else:
                messages.error(request, "Login failed!.")
                message = 'Login failed!'

            
    return render(request, 'tax-payers/login.html', context={'form': form, 'message': message})
    # context = {
    #     form: form
    # }
    # return render(request, 'login.html', context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            # print("I got here.....")

            print("REQUEST: ", user)
            login(request, user)
            return redirect("setup_profile")
    else:
        form = SignupForm()
    context = {
        form: form
    }
    return render(request, 'tax-payers/signup.html',{"form": form})


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    user = User.objects.get(id = request.user.id)
    print("Complete? ", user.is_profile_complete)
    if user.is_profile_complete:
        context = {
            "is_profile_complete" : True
        }
    context = {
         "is_profile_complete" : False
    }
    return render(request, 'tax-payers/dashboard.html', context)

@login_required
def setup_profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # print("PROFILE: ", form)
            profile = form.save(commit=False)
            profile.email = request.user.email
            profile.is_profile_complete = True
            profile.save()
            # user = user.update(
            #     company_name = form.cleaned_data['company_name'], 
            #     address = form.cleaned_data['address'],
            #     rc_number = form.cleaned_data['rc_number'],
            #     phone_number = form.cleaned_data['phone_number ' ],
            #     )
            messages.success(request, "Profile completed successfully")
            return redirect("dashboard")
        else:
            print("FORM IS INVALID.")
            print("ERRORS: ", form.errors)
        
    form = UserProfileForm(instance=user)
            
    context = {
        'form':form,
        'user':user,
    }
    return render(request, 'tax-payers/settings.html', context)