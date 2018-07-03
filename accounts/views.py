from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect   
from .forms import SignUpForm, UserForm   

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


def update_user(request):  
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            user=form.save(commit=False)    # 이 두 줄은 그냥 form.save() 만 해도 됨
            user.save()                      #이 두 줄은 그냥 form.save() 만 해도 됨
            return redirect('update_user')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'update_user.html', {'form': form})
