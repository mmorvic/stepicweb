from django.shortcuts import render
from django.http import HttpResponse
from qa.forms import SignupForm
from django.contrib.auth import authenticate, login


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def index(request):
    return render(request, 'index.html',
                  {'title': 'Latest',
                   'session': request.session, })



def question(request, num,):
    return render(request, 'question.html', 
    				{'num': num,
                    'session': request.session, })


def login(request):
    return render(request, 'login.html', {'session': request.session, })

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.raw_passeord
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form,
                                           'user': request.user,
                                           'session': request.session, })

def ask(request):
    return render(request, 'ask.html', {'session': request.session, })

def popular(request):
    return render(request, 'popular.html', {'session': request.session, })

def new(request):
    return render(request, 'new.html', {'session': request.session, })


