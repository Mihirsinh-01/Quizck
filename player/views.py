from django.shortcuts import render,redirect
from .models import Player
from host.models import Quiz
from .forms import playerForm
from django.http import HttpResponse
from firebase import firebase
import firebase_admin
from firebase_admin import db, credentials
from django.core import serializers
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

# print(firebase_admin.get_app())
print("Printed")
try:
    app = firebase_admin.get_app("Quizck")
except ValueError as e:
  print("Inside Value Error")
  cred = credentials.Certificate('host/templates/firebase.json')
  firebase_admin.initialize_app(cred,firebaseConfig)

dbRef = db.reference()


def joinplayer(request):
  if request.method == 'POST':
      form = playerForm(request.POST)
      if form.is_valid():
        gameid=request.POST['gameid']
        username=request.POST['username']
        if Player.objects.filter(gameId=gameid,username=username).exists():
          return HttpResponse("Username already Exists !!!")
        re=dbRef.child("games").get()
        print(re)
        print("HELLLOLLLLDDDS")
        if gameid in re:
          print("Yes Game Exists")
          playerLogin=Player(gameId=gameid,username=username)
          playerLogin.save()
          request.session["code"]=gameid
          nwplyr=dbRef.child("games").child(gameid).child("newplayer").get()
          nwplyr^=1
          dbRef.child("games").child(gameid).child("newplayer").set(nwplyr)
          print(nwplyr)
          return redirect('waiting')
        else:
          print("No game with such ID")
          return HttpResponse('No game with such ID')
        print(re)
        
  else:
      form = playerForm()

  return render(request, 'entergame.html', {'form': form})
