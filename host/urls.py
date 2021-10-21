from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('quiz',views.quiz,name='quiz'),
    path('createQuiz',views.createQuiz,name='createQuiz'),
    path('done',views.done,name='done'),
    path('quizPage/<int:pk>',views.quizPage,name='quizPage'),
    path('fbase',views.fbase,name='fbase'),
    path('tryy',views.tryy,name='tryy'),
    path('waiting',views.waiting,name="waiting"),
    path('showQuiz',views.showQuiz,name='showQuiz'),
    path('leaderboard',views.leaderboard,name='leaderboard'),
    path('temp',views.temp,name="temp"),
    path('tirth',views.tirth,name="tirth"),
    path('stats/<int:pk>',views.stats,name="stats")
]