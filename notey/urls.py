from notey.views import process_user
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register_user', views.process_user),
    path('feed', views.feed),
    path('login', views.login),
    path('logout', views.logout),
    path('user/<int:user_id>/me', views.my_profile),
    path('create/notebook', views.create_notebook),
    path('process_notebook', views.process_notebook),
    path('notebook/<int:notebook_id>', views.notebook),
    path('delete/<int:notebook_id>', views.delete),
    path('notebook/<int:notebook_id>/add_member', views.add_member),
    path('process_member/<int:notebook_id>', views.process_member),
    path('user/<int:user_id>', views.friend_page),
    path('notebook/<int:notebook_id>/add_page', views.add_page),
    path('process_page/<int:notebook_id>', views.process_page),
    path('notebook/<int:notebook_id>/<int:page_id>', views.edit_page),
    path('process_friend', views.add_friend),
    path('update_bio/<int:user_id>', views.update_bio),
    path('update_page/<int:page_id>/<int:notebook_id>', views.update_page)
]
