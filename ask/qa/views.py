import time
from django.shortcuts import render
from django.http import HttpResponse, Http404
from qa.forms import SignupForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qa.models import Question, Answer
from django.db.models import Max
from django.contrib.auth.models import User


def test(request, *args, **kwargs):
    return HttpResponse('OK')

def viewqs(request, question_list, limit=10):
    paginator = Paginator(question_list, limit) # Show lomit questions per page

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
             'paginator': paginator, }


def index(request):
    question_list = Question.objects.new()
    dic = viewqs(request, question_list)
    # paginator = Paginator(question_list, 10) # Show 10 questions per page

    # page = request.GET.get('page')
    # try:
    #     questions = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     questions = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     questions = paginator.page(paginator.num_pages)
    return render(request, 'index.html',
                  {'title': 'Questions',
                   'session': request.session, 
                   'questions': dic['questions'], 
                   'paginator': dic['paginator'],
                   'baseurl': '/?page=', 
                   })



def question(request, num,):
    try:
        question = Question.objects.get(id=num)
    except Question.DoesNotExist:
        raise Http404

    return render(request, 'question.html', 
    				{'num': num,
                    'session': request.session, 
                    'question': question, 
                    })


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
    question_list = Question.objects.popular()
    dic = viewqs(request, question_list)
    return render(request, 'index.html',
                  {'title': 'Popular',
                   'session': request.session, 
                   'questions': dic['questions'], 
                   'paginator': dic['paginator'], 
                   'baseurl': '/popular/?page=',                   
                   })

def new(request):
    return render(request, 'new.html', {'session': request.session, })

def initdb(request):
    res = Question.objects.all().aggregate(Max('rating'))
    max_rating = res['rating__max'] or 0
    user, _ = User.objects.get_or_create(username='test', password='test')
    for i in range(30):
        question = Question.objects.create(title='question ' + str(i), text='text ' + str(i),
                                           author=user, rating=max_rating + i)
    time.sleep(2)
    question = Question.objects.create(title='question last', text='text', author=user)
    question, _ = Question.objects.get_or_create(pk=3141592, title='question about pi',
                                                 text='what is the last digit?', author=user)
    question.answer_set.all().delete()
    for i in range(10):
        answer = Answer.objects.create(text='answer ' + str(i), question=question, author=user)

    return HttpResponse("Init done!")


