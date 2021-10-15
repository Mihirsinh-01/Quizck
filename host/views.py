from django.shortcuts import render
from player.models import Player
from .forms import createQuizForm
from .models import Quiz

# Create your views here.
def dashboard(req):
  players=Player.objects.filter(banned=False)
  alll=[]
  for player in players:
    alll.append(player['username'])
  return render(req,'dashboard.html',{'players':alll})

def createQuiz(req):
  if req.method == 'POST':
      form = createQuizForm(req.POST)
      if form.is_valid():
        # print("hii")
        questionNumber=req.POST['questionNumber']
        question=req.POST['question']
        option1=req.POST['option1']
        option2=req.POST['option2']
        option3=req.POST['option3']
        option4=req.POST['option4']
        answer=req.POST['answer']
        marks=req.POST['marks']
        timer=req.POST['timer']

        username=req.session['username'] 
               
        quiz=Quiz(hostname=username,)
        quiz.save()

        
        # return HttpResponse('/thanks/')
  else:
      form = createQuizForm()

  return render(req, 'createQuiz.html', {'form': form})  
