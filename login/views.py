from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import signupForm,loginForm
from .models import Login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt 
def signup(request):
  if request.method == 'POST':
      form = signupForm(request.POST)
      if form.is_valid():
        # print("hii")
        username=request.POST['username']
        password=request.POST['password']
        emailId=request.POST['emailId']
        
        checking=Login.objects.filter(username=username)
        if checking.exists():
          return render(request, 'signup.html', {'form': form})
        userLogin=Login(username=username,password=password,emailId=emailId)

        userLogin.save()

        
        # return HttpResponse('/thanks/')
  else:
      form = signupForm()

  return render(request, 'signup.html', {'form': form})

def login(request):
  if request.method == 'POST':
      form = loginForm(request.POST)
      if form.is_valid():
        # print("hii")
        username=request.POST['username']
        password=request.POST['password']
        
        checking=Login.objects.filter(username=username,password=password)
        if checking.exists():
          request.session['username']=username
          return redirect('dashboard')
        else:
          messages.error(request,'Enter valid data')

        
        # return HttpResponse('/thanks/')
  else:
      form = loginForm()

  return render(request, 'login.html', {'form': form})

# def dashboard(req):
#   return render(req,'dashboard.html')
  
