from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'The first name must be at least two characters long.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'The last name must be at least two characters long.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'The password must contain at least eight characters.'
        if postData['password'] != postData['confirm_password']:
            errors['no_match_pass'] = 'Error. Please ensure to confirm your password correctly.'
        for user in User.objects.all():
            if postData['email'] == user.email:
                errors['duplicate_email'] = 'This email is already registered to an account. Please enter a unique email.'
        return errors
        
    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) == 0:
            errors['email_existence'] = 'This user is not currently in our database. Please register first.'
            return errors
        user = User.objects.filter(email = postData['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                print('Password correct. Directing to next page...')
            else:
                errors['password'] = 'Incorrect password, please try again.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(default='')
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    objects = UserManager()
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notebook(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='notebooks', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='shared_notebooks')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Page(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(default='')
    notebook = models.ForeignKey(Notebook, related_name='pages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
