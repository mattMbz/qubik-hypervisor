from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from utils.validations import no_cache_render

@login_required
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '<strong>&#128516; Succesfully registration!</strong> '+'Account for user '+ user.username + ' was created successfully. Now you can Login!')
            return redirect('signin')
        #End_if
    else:
        form = CustomUserCreationForm()
        
    return no_cache_render(request, 'app_auth/signup.html', {'form' : form})
#End_def


def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
       
        if form.is_valid():
            print(f"Es valido")
            user = form.get_user()
            login(request, user)
            return redirect('mainpanel')
        else: 
            if (request.POST['password'] != '' or request.POST['username'] != ''):
                messages.error(request, ' <strong>&#9888</strong> Wrong username or password !')
                return redirect('signin')
    else:
        form = CustomAuthenticationForm()

    return no_cache_render(request, 'app_auth/signin.html', {'form': form})
#End_def


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
#End_def