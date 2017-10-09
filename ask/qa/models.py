from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(default='', max_length=256)
    text = models.TextField(default='')
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name="q_to_likes")
    objects = QuestionManager()

    def __unicode__(self):
        return self.title

    def get_url(self):
        return "/question/{}/".format(self.id)


class Answer(models.Model):
    text = models.TextField(default='')
    added_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.text


class NavBar:
    def __init__(self, active, typenav):
        self.active = active
        self.typenav = typenav  # False - login, True - logout
        self.data = ['navbar-nav mr-auto',
                     [
                         [u"Главная", '/'],
                         [u"По популярности", '/popular/?page=1'],
                         [u"Задать вопрос", '/ask/']
                     ]
                     ]

        self.data_login = []
        self.data_login.append(self.data)
        self.data_login.append(['navbar-nav ml-auto',
                                [
                                    [u"Вход", '/login/'],
                                    [u"Регистрация", '/signup/']]
                                ])

        self.data_logout = []
        self.data_logout.append(self.data)
        self.data_logout.append(['navbar-nav ml-auto',
                    [[u"Выход", '/logout/']]
                    ])
        self.get_current()

    def get_current(self):
        self.current = self.data_logout if self.typenav else self.data_login
    