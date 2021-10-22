from django.shortcuts import render, redirect
from django.core import serializers
from player.models import Player
from host.forms import createQuizForm
from host.models import Quiz, Game, Record
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
},name="game")
dbRef = db.reference()





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


def fbase(req):
  return HttpResponse('<script>window.location="waiting.html";</script>')
  


def tryy(req):
    return render(req, 'temp.html')

def tirth(req):
    return render(req, 'tirth.html')

def temp(req):

    from django.http import HttpResponse
    

    # List initialization
    list1 = ['Assam', 'India',
            'Lahore', 'Pakistan', 
            'New York', 'USA',
            'Bejing', 'China']
      
    df = pd.DataFrame()
      
    # Creating two columns
    df['State'] = list1[0::2]
    df['Country'] = list1[1::2]


    # df['Player']

    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    
  
    
      
    # Converting to excel
    # df.to_excel('result.xlsx', index = False)
    # return render(req,'temp.html')
    # from io import StringIO
    # from xhtml2pdf import pisa
    # from django.template.loader import get_template
    # from django.template import Context
    # from django.http import HttpResponse
    # import numpy
    # # from cgi import escape

    # template = get_template("temp.html")
    # context = Context()
    # html  = template.render({"radhe":"shyam"})
    # result = StringIO()
    # # numpy.genfromtxt(io.BytesIO(x.encode()))
    # z=html.encode("UTF-8")
    # print(type(z))
    # x=numpy.genfromtxt(z)
    # y=StringIO(x)
    # pdf = pisa.pisaDocument(y, result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    # print("temp function is called")


def waiting(req):
    global globReq
    
    gameId = req.session["code"]
    globReq = req
    path='games/'+gameId
    db.reference(path).listen(strm)

    games=list(Game.objects.all())
    for x in games:
      if gameId in x.gameId.split(","):
        req.session['hostname']=x.hostname
        req.session['quizId']=x.quizId
        break

    req.session['questionNumber']=0

    if req.session['user'] == 'player':
      return render(req, 'waiting.html', { 'code': req.session["code"], 'user':req.session['user'], 'playername':req.session['playername']})
    else:
      return render(req, 'waiting.html', { 'code': req.session["code"], 'user':req.session['user']})


def showQuiz(req):
  questionNumber=req.session['questionNumber']+1
  req.session['questionNumber']=questionNumber
  cnt=Quiz.objects.filter(hostname=req.session['hostname'],quizId=req.session['quizId']).count()
  print("Count is ",cnt)
  print("Current Question is ",questionNumber)
  if questionNumber>cnt:
    return redirect('tryy')
  else:
    qz=Quiz.objects.filter(hostname=req.session['hostname'],quizId=req.session['quizId'],questionNumber=questionNumber)[0]
    return render(req,"showQuiz.html",{"quiz":qz})

def leaderboard(req):
  answer=req.POST.get('options')
  gameId=req.session['code']
  host=req.session['hostname']
  quizId=req.session['quizId']

  

  ques=list(Quiz.objects.filter(quizId=quizId,questionNumber=req.session['questionNumber'],hostname=host))
  if len(ques)==0:
    return HttpResponse("<h1>Questions Exceeded in Leaderboard</h1>")
  ques=ques[0]
  marks=0
  if ques.answer == answer:
    marks=ques.marks
  if(req.session['user']=='player'):
    rec=list(Record.objects.filter(gameId=gameId,playername=req.session['playername']))
    if len(rec)==0:
      Record(gameId=gameId, quizId=quizId, marks=str(marks), playername=req.session['playername']).save()
    else:
      rec=rec[0]
      a=rec.marks.split(",")
      if req.session['questionNumber']-1 <= len(a):
        a.append(str(marks))
        a=",".join(a)
        rec.marks=a
        rec.save()
  
  players=dbRef.child("games").child(gameId).child("newplayer").get()

  lead=[]
  while True:
    lead=list(Record.objects.filter(quizId=quizId,gameId=gameId))
    if(len(lead)==len(players)-1):
      flag=False
      for x in lead:
        if len(x.marks.split(","))!=req.session['questionNumber']:
          flag=True
      if not flag:
        break
    else:
      time.sleep(1)
  allPlayer=[]
  for item in lead:
    allmarks=item.marks.split(",")
    total=0
    for mrk in allmarks:
      total+=int(mrk)
    if allmarks[len(allmarks)-1]=="0":
      tot=str(total)+' (0)'
    else:
      tot=str(total)+" (+"+str(allmarks[len(allmarks)-1])+")"
    allPlayer.append([total,[item.playername,tot]])
    # allPlayer[total]=[item.playername,tot]
  
  x=allPlayer.sort(reverse=True)
  # x=dict(sorted(allPlayer.items(),reverse=True))
  print(x)
  leader=[y for x,y in allPlayer] 
  print(leader)

  print("LeaderBoard Printed")

  return render(req,'leaderboard.html',{"leaderboard":leader,"user":req.session['user'],"code":req.session['code']})



def download(req,**pk):
  game=pk['game'].split(",")
  gameId,quizId=game
  records=list(Record.objects.filter(gameId=gameId,quizId=quizId))
  questions=list(Quiz.objects.filter(hostname=req.session['username'],quizId=quizId))
  
  df = pd.DataFrame()
  df1 = pd.DataFrame()

  ques=[]
  options=[]
  for que in questions:
    x=[]
    y=[]
    x.append(que.question)
    x.append(que.answer)
    x.append(que.marks)
    y.append(que.option1)
    y.append(que.option2)
    y.append(que.option3)
    y.append(que.option4)
    ques.append(x)
    options.append(y)
  
  df['Questions']=[x[0] for x in ques]
  # df['Answers']=[x[1] for x in ques]
  df['Marks']=[x[2] for x in ques]
  ans=[]
  for i in range(len(ques)):
    ans.append(options[i][int(ques[i][1])-1])
  df['Answers']=ans #[x for x in ans]

  
  lists=[]
  for record in records:
    player=record.playername
    marks=record.marks.split(",")
    total=0
    for x in marks:
      total+=int(x)
    marks.insert(0, player)
    marks.insert(len(marks)-1, total)
    lists.append(marks)
  
  s="Question"
  if lists:
    df1['Player Name']=[x[0] for x in lists]
    for i in range(1,len(lists)):
      df1[s+str(i)] = [x[i] for x in lists]
    df1['Total Marks']=[x[len(lists)] for x in lists]
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Questions')
        df1.to_excel(writer, sheet_name='Marksheet')
        writer.save()
        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    
    print(df1)
    return HttpResponse("hiii")
  else:
    print("no data")
    return HttpResponse("No data is found")



def removed(req):
  player=req.session['playername']
  plyr=Player.objects.filter(username=player,gameId=req.session['code'])
  plyr[0].banned=True
  plyr[0].save()
  messages.error(req,"You got Banned !!")
  return redirect('join')