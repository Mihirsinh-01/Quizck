from django.shortcuts import render, redirect
from django.core import serializers
from player.models import Player
from .forms import createQuizForm
from .models import Quiz, Game, Record
from django.http import HttpResponse
import json
import shortuuid
import firebase_admin
from firebase_admin import db, credentials
import datetime,pytz
import time
from io import BytesIO
import pandas as pd
from django.contrib import messages

# mihir firebase
firebaseConfig = {
  "apiKey": "AIzaSyDNn1-wkMm-g0cH2BKQ6XjdLTl6ldds8ZE",
  "authDomain": "quizck-74e04.firebaseapp.com",
  "projectId": "quizck-74e04",
  "storageBucket": "quizck-74e04.appspot.com",
  "messagingSenderId": "555502389734",
  "appId": "1:555502389734:web:2a977e89e54df3c69cae27",
  "measurementId": "G-XFLZV89Q56",
  "databaseURL": "https://quizck-74e04-default-rtdb.firebaseio.com/"
}

## dhvanik firebase
# firebaseConfig = {
#   "apiKey": "AIzaSyCHL_LDHGj7MLqNDOMDhkpxuW_3HPyizAA",
#   "authDomain": "quizck-4548a.firebaseapp.com",
#   "projectId": "quizck-4548a",
#   "storageBucket": "quizck-4548a.appspot.com",
#   "messagingSenderId": "418637328890",
#   "appId": "1:418637328890:web:cf263d4febbff817c63443",
#   "measurementId": "G-WE6D793S4X",
#   "databaseURL":"https://quizck-4548a-default-rtdb.firebaseio.com/"
#   };

import firebase_admin
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="host/templates/firebase.json"

cred=credentials.Certificate('host/templates/firebase.json')
fireapp=firebase_admin.initialize_app(cred,{
  "databaseURL":"https://quizck-74e04-default-rtdb.firebaseio.com/"
},name="host")
dbRef = db.reference()


def dashboard(req):

    username = req.session['username']
    quiz = Quiz.objects.filter(hostname=username).values_list(
        'quizId', flat=True).distinct()
    quizzes = []
    i = 1
    for x in quiz:
        quizzes.append([i, x])
        i += 1
    return render(req, 'dashboard.html', {'quizzes': quizzes})


def quiz(req):
    username = req.session['username']
    temp = Quiz.objects.filter(hostname=username).values_list('quizId',flat=True)
    mx = 0
    for x in temp:
      mx = max(mx, x)
    req.session['quizId'] = mx + 1
    return redirect('createQuiz')


def createQuiz(req):
    if req.method == 'POST':
        form = createQuizForm(req.POST)
        if form.is_valid():
            cnt=Quiz.objects.filter(quizId=req.session['quizId'],hostname=req.session['username']).count()
            questionNumber = cnt+1
            question = req.POST['question']
            option1 = req.POST['option1']
            option2 = req.POST['option2']
            option3 = req.POST['option3']
            option4 = req.POST['option4']
            answer = req.POST['answer']
            marks = req.POST['marks']
            timer = req.POST['timer']

            username = req.session['username']
            quizId = req.session['quizId']

            quiz = Quiz(hostname=username,
                        quizId=quizId,
                        questionNumber=questionNumber,
                        question=question,
                        option1=option1,
                        option2=option2,
                        option3=option3,
                        option4=option4,
                        answer=answer,
                        marks=marks,
                        timer=timer)

            quiz.save()
            form = createQuizForm()
    else:
        form = createQuizForm()
        print(type(form))

    return render(req, 'createQuiz.html', {'form': form})


def done(req):
    if req.method == 'POST':
        form = createQuizForm(req.POST)
        if form.is_valid():
          cnt=Quiz.objects.filter(quizId=req.session['quizId'],hostname=req.session['username']).count()
          questionNumber = cnt+1
          question = req.POST['question']
          option1 = req.POST['option1']
          option2 = req.POST['option2']
          option3 = req.POST['option3']
          option4 = req.POST['option4']
          answer = req.POST['answer']
          marks = req.POST['marks']
          timer = req.POST['timer']

          username = req.session['username']
          quizId = req.session['quizId']

          quiz = Quiz(hostname=username,quizId=quizId,questionNumber=questionNumber,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=marks,timer=timer)

          
          quiz.save()

    return redirect('dashboard')
    
def stats(req, **primarykey):
  quizId=primarykey['pk']
  hostname=req.session['username']
  game=list(Game.objects.filter(hostname=hostname,quizId=quizId))
  if not game:
    return render(req,'stats.html',{"quizId":quizId,"games":[]})
  game=game[0]
  gameIds=game.gameId.split(",")
  gameTimes=game.gameTime.split(",")
  games=[]
  for i in range(len(gameIds)):
    games.append([gameIds[i],gameTimes[i]])

  games.sort(key = lambda x: x[1])
  print(games)
  return render(req,'stats.html',{"games":games,"quizId":quizId})

def quizPage(req, **primarykey):
    quizId = primarykey['pk']
    qz = Quiz.objects.filter(quizId=quizId, hostname=req.session["username"])
    qz = serializers.serialize('json', qz)
    qz = json.loads(qz)
    code = shortuuid.ShortUUID().random(length=2)
    req.session["code"] = code
    req.session['user']="admin"
    req.session['quizId']=quizId
    

    username = req.session['username']
    quizId = req.session['quizId']
    dt=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    
    game=list(Game.objects.filter(hostname=username,quizId=quizId))
    if len(game)==0:
      game=Game(hostname=username,quizId=quizId,gameId=code,gameTime=dt.strftime("%b %d %Y %H:%M:%S"))
      game.save()
    else:
      game=game[0]
      gameId=game.gameId.split(",")
      gameTime=game.gameTime.split(",")
      gameId.append(code)
      gameTime.append(dt.strftime("%b %d %Y %H:%M:%S"))
      game.gameId=",".join(gameId)
      game.gameTime=",".join(gameTime)

      game.save()

    dbRef.child("games").child(code).set({
      'host': req.session["username"],
      'next': 0,
      'newplayer': [''],
      'started':0
    })

    return render(req, 'quizPage.html', {
      "sec": 105,
      "query": qz,
      "code": code
    })


globReq = ""

def strm(message):
  print('inside strm function')
  print()
  qz = globReq.session["code"]
  players = Player.objects.filter(banned=False,gameId=qz).values_list('username',flat=True)
  alll = []
  for player in players:
    alll.append(player)
  print("Data Changed")
  if 'username' in globReq.session:
    print(globReq.session['username'])
    print("List of Players: ")
    print(alll)
  else:
    print("other user")
  return redirect('fbase')
  print('end of strm function')


