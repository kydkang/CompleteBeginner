from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect   
from .forms import SignUpForm  

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)       
        if form.is_valid():
            user = form.save()                       ## a User instance is created
            auth_login(request, user)                  ## authenticate the user  
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
