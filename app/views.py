from django.shortcuts import render,HttpResponse
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')

def Registration(request):                                                                                           
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            nsuo=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            nsuo.set_password(password)
            nsuo.save()

            nspo=pfd.save(commit=False)
            nspo.username=nsuo

            nspo.save()
            return HttpResponse('data insertted succesfull')
        else:
            return HttpResponse('Please Fill All The data...!')

    return render(request,'Registration.html',d)

def login_form(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        lio=authenticate(username=username,password=password)
        if lio is not None:
            login(request,lio)
            request.session['username']=username

            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password....!')


    return render(request,'login_form.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def change_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(password)
        UO.save()
        return HttpResponse('Password is changed successfull....!')

    return render(request,'change_password.html')



def forgot_pw(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        fo=User.objects.filter(username=username)
        if fo:
            fo[0].set_password(password)
            fo[0].save()
            return HttpResponse('Reset password successfull..!')
        else:
            return HttpResponse('User name is not available...!')
            
    return render(request,'forgot_pw.html')