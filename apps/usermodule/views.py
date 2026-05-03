from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error in registration. Please check the form.')
    else:
        form = UserCreationForm()
    return render(request, 'usermodule/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successfully!')
            
            return redirect('/books/lab11/task2/students') 
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'usermodule/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')