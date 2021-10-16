from django.shortcuts import render,redirect
from django.core import serializers
from player.models import Player
from .forms import createQuizForm
from .models import Quiz
from django.http import HttpResponse
import pyrebase
import json
import shortuuid

firebaseConfig = {
    "apiKey": "AIzaSyDNn1-wkMm-g0cH2BKQ6XjdLTl6ldds8ZE",
    "authDomain": "quizck-74e04.firebaseapp.com",
    "projectId": "quizck-74e04",
    "storageBucket": "quizck-74e04.appspot.com",
    "messagingSenderId": "555502389734",
    "appId": "1:555502389734:web:2a977e89e54df3c69cae27",
    "measurementId": "G-XFLZV89Q56",
    "databaseURL":"https://quizck-74e04-default-rtdb.firebaseio.com/"
  };
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()



def dashboard(req):
  
  username=req.session['username']
  quiz=Quiz.objects.filter(hostname=username).values_list('quizId',flat=True).distinct()
  quizzes=[]
  i=1
  for x in quiz:
    quizzes.append([i,x])
    i+=1
  return render(req,'dashboard.html',{'quizzes':quizzes})


def quiz(req):
  username=req.session['username']
  temp=Quiz.objects.filter(hostname=username).values_list('quizId',flat=True)
  mx=0
  for x in temp:
    mx=max(mx,x)
  req.session['quizId']=mx+1
  return redirect('createQuiz')


def createQuiz(req):
  if req.method == 'POST':
      form = createQuizForm(req.POST)
      if form.is_valid():
        questionNumber=req.POST['question_Number']
        question=req.POST['question']
        option1=req.POST['option1']
        option2=req.POST['option2']
        option3=req.POST['option3']
        option4=req.POST['option4']
        answer=req.POST['answer']
        marks=req.POST['marks']
        timer=req.POST['timer']

        username=req.session['username'] 
        quizId=req.session['quizId']

        quiz=Quiz(hostname=username,quizId=quizId,questionNumber=questionNumber,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=marks,timer=timer)
        
        quiz.save()
        form=createQuizForm()
  else:
      form = createQuizForm()
      print(type(form))

  return render(req, 'createQuiz.html', {'form': form})

def done(req):
  if req.method == 'POST':
      form = createQuizForm(req.POST)
      if form.is_valid():
        questionNumber=req.POST['question_Number']
        question=req.POST['question']
        option1=req.POST['option1']
        option2=req.POST['option2']
        option3=req.POST['option3']
        option4=req.POST['option4']
        answer=req.POST['answer']
        marks=req.POST['marks']
        timer=req.POST['timer']

        username=req.session['username'] 
        quizId=req.session['quizId']

        quiz=Quiz(hostname=username,quizId=quizId,questionNumber=questionNumber,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=marks,timer=timer)
        
        quiz.save()
  

  return redirect('dashboard')


def quizPage(req,**primarykey):
  x=primarykey['pk']
  qz=Quiz.objects.filter(quizId=x,hostname=req.session["username"])
  qz=serializers.serialize('json',qz)
  qz=json.loads(qz)
  print(type(qz))
  print(qz)
  print("Done")  
  code = shortuuid.ShortUUID().random(length=4)
  db.child("games").child(code).set({'host':req.session["username"],'next':0})
  req.session["code"]=code


  return render(req,'quizPage.html',{"sec":105,"query":qz,"code":code})

def strm(message):
  print(message)
  print("Data Changed")

def fbase(req):
  
  db.child("Custom Key").stream(strm)
  db.child("Custom Key").set({"name":"Mihir","surname":"Vaja"})
  return HttpResponse("<b>Data Pushed in Firebase</b>")

def tryy(req):
  return render(req,'temp.html')

def waiting(req):
  qz=req.session["code"]
  players=Player.objects.filter(banned=False,gameId=qz).values_list('username',flat=True)
  alll=[]

  for player in players:
    alll.append(player)

  return render(req,'waiting.html',{'players':alll,'code':req.session["code"]})