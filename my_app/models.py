from django.db import models
import bcrypt,re


class UserManager(models.Manager):
    def user_validator(self,postData):
        errors={}
        if not str(postData['first_name']).isalpha():
            errors['first_name']="first name should be alphapitical latters"
        if not str(postData['last_name']).isalpha():
            errors['last_name']="last name should be alphapitical latters"
        if len(postData['first_name'])<3:
            errors['first_name']="first name should be at least 3 characters"
        if len(postData['first_name'])<3:
            errors['last_name']="last name should be at least 3 characters" 
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email']))>0:
            errors['email']=f"this email {postData['email']} already have user"
        
        if len(postData['password'])<8:
            errors['password']="password should be at least 8 characters"
        if postData['password']!=postData['password_confirm']:
            errors['password_confirm']="passwords doesnt match"
        return errors

    def login_validator(self,postData):
        errors={}
        my_user=User.objects.filter(email=postData['email'])
        if len(my_user)==0:
            errors['email']=f"this email {postData['email']} have no account, please enter correct email or go to sign up to create a new user"
        else:
            real_password=my_user[0].password
            if  not bcrypt.checkpw(postData['password'].encode(), real_password.encode()):
                errors['password']="incorrect password please try again"
        return errors


class PyPieManager(models.Manager):
    def pie_validator(self,postData):
        errors={}
        if len(postData['name'])<2:
            errors['name']=" name should be at least 2 characters"
        if len(postData['filling'])<2:
            errors['filling']=" filling should be at least 2 characters"
        if len(postData['crust'])<2:
            errors['crust']=" crust should be at least 2 characters"
        return errors

class User (models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #my_pies
    #liked_pies
    objects=UserManager()



class PyPie(models.Model):
    name=models.CharField(max_length=255)
    filling=models.TextField()
    crust=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name='my_pies',on_delete=models.CASCADE)
    votes= models.ManyToManyField(User, related_name="liked_pies")
    objects=PyPieManager()

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password
def create_user(first_name,last_name,email,password):
    new_user= User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hash_password(password))
    return new_user.id

def logged_user(email):
    my_users=User.objects.filter(email=email)
    my_user=my_users[0]
    return my_user.id

def create_pie(name,filling,crust,user_id):
    user=User.objects.get(id=user_id)
    PyPie.objects.create( name=name,filling=filling,crust=crust,user=user)

def get_pie(id):
    pie= PyPie.objects.get(id=id)
    return pie
def get_user(id):
    user= User.objects.get(id=id)
    return User

def edit_my_pie(pi_id,name,filling,crust):
    pie=PyPie.objects.get(id=pi_id)
    pie.name=name
    pie.filling=filling
    pie.crust=crust
    pie.save()

def get_all_pies():
    return PyPie.objects.all()

def get_liked_pies(user_id):
    user=User.objects.get(id=user_id)
    return user.liked_pies.all()

def add_like(userID,pieID):
    pie= PyPie.objects.get(id=pieID)
    user= User.objects.get(id=userID)
    pie.votes.add(user)


def delete_pie(id):
    pie=PyPie.objects.get(id=id)
    pie.delete()


def remove_like(userID,pieID):
    pie= PyPie.objects.get(id=pieID)
    user= User.objects.get(id=userID)
    user.liked_pies.remove(pie)