from django.shortcuts import render,redirect
from .models import Player
from host.models import Quiz
from .forms import playerForm
from django.http import HttpResponse
from firebase import firebase
import firebase_admin
from firebase_admin import db, credentials
from django.core import serializers
from django.contrib import messages
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="host/templates/firebase.json"



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

try:
    app = firebase_admin.get_app("Quizck")
except ValueError as e:
  print("Inside Value Error")
  cred = credentials.Certificate('host/templates/firebase.json')
  firebase_admin.initialize_app(cred,firebaseConfig)

dbRef = db.reference()


def joinplayer(request):
  gameid=""
  username=""
  if request.method == 'POST':
      form = playerForm(request.POST)
      if form.is_valid():
        gameid=request.POST['gameid']
        username=request.POST['username']        
        re=dbRef.child("games").get()
        if re and gameid in re:
          if re[gameid]['started']==1:
            messages.error(request,"Game has already started !!")
            return render(request, 'entergame.html', {'gameid': gameid,"username":username})
          if Player.objects.filter(gameId=gameid,username=username).exists():
            messages.error(request,"Username already Exists !!!")
            return render(request, 'entergame.html', {'gameid': gameid,"username":username})
          playerLogin=Player(gameId=gameid,username=username)
          playerLogin.save()
          request.session["code"]=gameid
          nwplyr=dbRef.child("games").child(gameid).child("newplayer").get()
          try:
            nwplyr.append(username)
          except:
            nwplyr=[username]
          dbRef.child("games").child(gameid).child("newplayer").set(nwplyr)
          
          request.session['user']="player"
          request.session['playername']=username
          return redirect('waiting')
        else:
          messages.error(request,"No game with such ID")
        
  else:
      form = playerForm()

  return render(request, 'entergame.html', {'gameid': gameid,"username":username})
