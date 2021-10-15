from django.shortcuts import render,redirect
from player.models import Player
from .forms import createQuizForm
from .models import Quiz

# Create your views here.
def dashboard(req):
  players=Player.objects.filter(banned=False).values_list('username',flat=True)
  alll=[]

  for player in players:
    alll.append(player)

  username=req.session['username']
  quiz=Quiz.objects.filter(hostname=username).values_list('quizId',flat=True).distinct()
  quizzes=[]

  i=1
  for x in quiz:
    quizzes.append([i,x])
    i+=1
  return render(req,'dashboard.html',{'players':alll,'quizzes':quizzes})


def quiz(req):
  username=req.session['username']
  temp=Quiz.objects.filter(hostname=username).values_list('quizId',flat=True)
  mx=0
  for x in temp:
    mx=max(mx,x)
  req.session['quizId']=mx+1
  return redirect('createQuiz')


def createQuiz(req):
  print("Inside Create Quiz")
  if req.method == 'POST':
      form = createQuizForm(req.POST)
      if form.is_valid():
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
        quizId=req.session['quizId']

        quiz=Quiz(hostname=username,quizId=quizId,questionNumber=questionNumber,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=marks,timer=timer)
        
        quiz.save()
  

  return redirect('dashboard')


def quizPage(req):
  
