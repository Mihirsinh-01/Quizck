from django.shortcuts import render,redirect
from .models import Player
from host.models import Quiz
from .forms import playerForm
from django.http import HttpResponse
from firebase import firebase


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
firebase = firebase.FirebaseApplication('https://quizck-74e04-default-rtdb.firebaseio.com/', None)
# firebase=pyrebase.initialize_app(firebaseConfig)
# db=firebase.database()
db=firebase


def joinplayer(request):
  if request.method == 'POST':
      form = playerForm(request.POST)
      if form.is_valid():
        gameid=request.POST['gameid']
        username=request.POST['username']
        if Player.objects.filter(gameId=gameid,username=username).exists():
          return HttpResponse("Username already Exists !!!")
        re=list(db.child("games").shallow().get().val())
        if gameid in re:
          print("Yes Game Exists")
          playerLogin=Player(gameId=gameid,username=username)
          playerLogin.save()
          request.session["code"]=gameid
          nwplyr=db.child("games").child(gameid).child("newplayer").get().val()
          nwplyr^=1
          db.child("games").child(gameid).child("newplayer").set(nwplyr)
          print(nwplyr)
          return redirect('waiting')
        else:
          print("No game with such ID")
          return HttpResponse('No game with such ID')
        print(re)
        
  else:
      form = playerForm()

  return render(request, 'entergame.html', {'form': form})
