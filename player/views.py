from django.shortcuts import render
from .models import Player
from .forms import playerForm
from django.http import HttpResponse

def joinplayer(request):
  if request.method == 'POST':
      form = playerForm(request.POST)
      if form.is_valid():
        gameid=request.POST['gameid']
        username=request.POST['username']
        if Player.objects.filter(gameId=gameid,username=username).exists():
          return HttpResponse("Username already Exists !!!")
        playerLogin=Player(gameId=gameid,username=username)
        playerLogin.save()
        
        return HttpResponse('/thanks/')
  else:
      form = playerForm()

  return render(request, 'entergame.html', {'form': form})
