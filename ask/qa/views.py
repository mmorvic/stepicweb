import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from qa.forms import SignupForm, AskForm, AnswerForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qa.models import Question, Answer, NavBar
from django.db.models import Max
from django.contrib.auth.models import User
# import logging


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def createNavbar(active, request):
    navbar = NavBar(active, request.user.is_authenticated)
    # navbar.typenav = request.user.is_authenticated
    # navbar.get_current()
    # logging.basicConfig(level = logging.DEBUG)
    # logging.debug('active is ', navbar.active, 'current', navbar.current)
    # navbar.active = active
    return navbar    


def viewqs(request, question_list, active, limit=10):
    paginator = Paginator(question_list, limit) # Show lomit questions per page
    navbar = createNavbar(active, request)
    page = request.GET.get('page')

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return { 'questions': questions, 
             'paginator': paginator, 
             'navbar': navbar, }


def index(request):
    question_list = Question.objects.new()
    dic = viewqs(request, question_list, u"Главная")

    return render(request, 'index.html',
                  {'title': 'Questions',
                   'session': request.session, 
                   'questions': dic['questions'], 
                   'paginator': dic['paginator'],
                   'navbar': dic['navbar'],
                   'baseurl': '/?page=', 
                   })



def question(request, num,):
    try:
        question = Question.objects.get(id=num)
    except Question.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            post = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})

    return render(request, 'question.html', {'question': question,
                                             'form': form,
                                             'user': request.user,
                                             'session': request.session, })



def login_view(request):
    navbar = createNavbar(u"Вход", request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # print('save form')
            username = form.cleaned_data["username"]
            password = form.raw_passeord
            user = authenticate(username=username, password=password)
            # print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()    
    return render(request, 'login.html', 
        {'form': form,
         'navbar': navbar,
         'user': request.user,
         'session': request.session, })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    navbar = createNavbar(u"Регистрация", request)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('save form')
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.raw_passeord
            # user = User.objects.create_user(username, email=email, password=password)
            # user.save()
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form,
                                           'navbar': navbar,
                                           'user': request.user,
                                           'session': request.session, })

def ask(request):
    navbar = createNavbar(u"Задать вопрос", request)
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form': form,
                                        'navbar': navbar,
                                        'user': request.user,
                                        'session': request.session, })


def popular(request):
    question_list = Question.objects.popular()
    dic = viewqs(request, question_list, u"По популярности")
    return render(request, 'index.html',
                  {'title': 'Popular',
                   'session': request.session, 
                   'questions': dic['questions'], 
                   'paginator': dic['paginator'],
                   'navbar': dic['navbar'], 
                   'baseurl': '/popular/?page=',                   
                   })

def new(request):
    return render(request, 'new.html', {'session': request.session, })

def initdb(request):
    res = Question.objects.all().aggregate(Max('rating'))
    max_rating = res['rating__max'] or 0
    user, _ = User.objects.get_or_create(username='test', password='test')
    for i in range(30):
        question = Question.objects.create(title='question ' + '200' + str(i), text='text ' + str(i),
                                           author=user, rating=max_rating + i)
        time.sleep(2)
    # question = Question.objects.create(title='question last', text='text', author=user)
    # question, _ = Question.objects.get_or_create(pk=3141592, title='question about pi',
    #                                              text='what is the last digit?', author=user)
    question.answer_set.all().delete()
    for i in range(10):
        answer = Answer.objects.create(text='answer ' + str(i), question=question, author=user)

    return HttpResponse("Init done!")


