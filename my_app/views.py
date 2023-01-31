from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
# Create your views here.
def run(request):
    return render(request,'index.html')


def regester(request):
    errors=User.objects.user_validator(request.POST)
    first_name= request.POST['first_name']
    last_name= request.POST['last_name']
    email= request.POST['email']
    password= request.POST['password']
    context={'first_name':request.POST['first_name'],
            'last_name':request.POST['last_name'],
            'email':request.POST['email'],
    }
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request,'index.html', context)
    else:
        request.session['current_user_id']=create_user(first_name,last_name,email,password)
    return redirect('/')

def login(request):
    errors=User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email=request.POST['email']
        logged_user_id=logged_user(email)
        request.session['current_user_id']=logged_user_id
        return redirect('/my_pies')



def my_pies(request):
    my_user=User.objects.get(id=request.session['current_user_id'])
    context={
        'user':my_user,
        'pies': my_user.my_pies.all().order_by('-created_at')
    }
    return render (request,'my_pies.html',context)

def add_pie(request):
    errors= PyPie.objects.pie_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/my_pies')
    else:
        name=request.POST['name']
        filling=request.POST['filling']
        crust=request.POST['crust']
        user_id=request.session['current_user_id']
        create_pie(name,filling,crust,user_id)
        return redirect('/my_pies')


def edit(request,id):
    pie=get_pie(id)
    context={
        'pie':pie
    }
    return render(request,'edit.html',context)

def edit_pie(request):
    pi_id=request.POST['pie_id']
    pie_id=int(pi_id)
    errors= PyPie.objects.pie_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit/{pie_id}")
    else:
        pi_id=request.POST['pie_id']
        name=request.POST['name']
        filling=request.POST['filling']
        crust=request.POST['crust']
        edit_my_pie(pi_id,name,filling,crust)
        return redirect('/my_pies')


def derby(request):
    context={
        'pies':get_all_pies(),
        'user':get_user(request.session['current_user_id']),
    }
    return render (request,'derby.html',context)


def vote(request,id):
    context={
        "pie":get_pie(id),
        "user":get_user(request.session['current_user_id']),
        "liked_pies":get_liked_pies(request.session['current_user_id'])
    }
    return render(request,'vote.html',context)

def do_like(request):
    pie_id=request.POST['pie_id']
    userID=request.session['current_user_id']
    add_like(userID,pie_id)
    return redirect('/derby')

def delete (request,id):
    delete_pie(id)
    return redirect ('/my_pies')


def logout(request):
    del request.session['current_user_id']
    return redirect('/')

def dislike(request):
    pie_id=request.POST['pie_id']
    userID=request.session['current_user_id']
    remove_like(userID,pie_id)
    return redirect(f'vote/{pie_id}')   