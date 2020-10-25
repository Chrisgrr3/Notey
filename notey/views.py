from django.contrib import messages
from django.http import request
from django.shortcuts import redirect, render
from .models import *
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }
    return render(request, 'landing.html', context)

def process_user(request):
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    entered_password = request.POST['password']
    hash_pass = bcrypt.hashpw(entered_password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name= request.POST['first_name'],
        last_name= request.POST['last_name'],
        password = hash_pass,
        email = request.POST['email']
    )
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/feed')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request,value)
        return render (request,'landing.html')
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/feed')

def feed(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'logged_in_user': this_user,
        'my_notebooks': this_user.notebooks.all(),
        'shared_notebooks': this_user.shared_notebooks.all(),
    }
    return render(request,'feed.html',context)

def delete(request, notebook_id):
    this_notebook = Notebook.objects.get(id = notebook_id)
    this_notebook.delete()
    return redirect('/feed')


def my_profile(request, user_id):
    this_user = User.objects.get(id = user_id)
    context = {
        "user": this_user,
        "my_notebooks": this_user.notebooks.all(),
        "shared_notebooks": this_user.shared_notebooks.all()
    }
    return render(request,'profile.html', context)

def update_bio(request,user_id):
    this_user = User.objects.get(id = user_id)
    this_user.bio = request.POST['bio']
    this_user.save()
    return redirect(f'/user/{user_id}/me')

def create_notebook(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'me': this_user,
        'users': User.objects.all()
    }
    return render(request, 'create_notebook.html', context)

def process_notebook(request):
    Notebook.objects.create(
        title = request.POST['title'],
        creator = User.objects.get(id = request.session['user_id']),
        is_public = request.POST['type']
    )
    this_notebook_id = Notebook.objects.last().id
    return redirect(f'/notebook/{this_notebook_id}')

def notebook(request, notebook_id):
    this_notebook = Notebook.objects.get(id=notebook_id)
    if this_notebook.is_public == True:
        members = this_notebook.members.all()
        context = {
            'notebook': this_notebook,
            'is_public': True,
            'members': members
        }
        return render(request,'notebook.html', context)
    context = {
        'notebook': this_notebook,
        'is_private': True
    }
    return render(request,'notebook.html', context)

def add_member(request, notebook_id):
    context = {
        'notebook': Notebook.objects.get(id = notebook_id)
    }
    return render(request, 'add_member.html', context)

def process_member(request, notebook_id):
    this_notebook = Notebook.objects.get(id = notebook_id)
    this_member = User.objects.get(email = request.POST['add'])
    this_notebook.members.add(this_member)
    this_notebook.save()
    return redirect(f'/notebook/{this_notebook.id}')

def friend_page(request,user_id):
    context = {
        'my_friend': User.objects.get(id = user_id)
    }
    return render(request, 'friend_profile.html', context)

def add_page(request,notebook_id):
    this_notebook = Notebook.objects.get(id = notebook_id)
    context = {
        'this_notebook': this_notebook
    }
    return render(request, 'add_page.html', context)

def process_page(request,notebook_id):
    this_notebook = Notebook.objects.get(id = notebook_id)
    Page.objects.create(
        title = request.POST['page_title'],
        notebook = this_notebook,
    )
    return redirect(f'/notebook/{notebook_id}')

def edit_page(request, notebook_id, page_id):
    this_notebook = Notebook.objects.get(id=notebook_id)
    this_page = Page.objects.get(id=page_id)
    context = {
        'notebook': this_notebook,
        'page': this_page
    }
    return render(request,'edit_page.html', context)

def update_page(request,page_id,notebook_id):
    this_page = Page.objects.get(id = page_id)
    this_page.notes = request.POST['note']
    this_page.save()
    this_notebook = Notebook.objects.get(id = notebook_id)
    return redirect(f'/notebook/{this_notebook.id}/{page_id}')

def add_friend(request):
    this_friend = User.objects.get(email = request.POST['email'])
    this_user = User.objects.get(id = request.session['user_id'])
    this_user.friends.add(this_friend)
    return redirect('/feed')

def logout(request):
    request.session.flush()
    return redirect('/')