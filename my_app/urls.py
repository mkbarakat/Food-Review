from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.run),
    path('regester', views.regester),
    path('login', views.login),
    path('my_pies', views.my_pies),
    path('add_pie', views.add_pie),
    path('edit/<int:id>', views.edit),
    path('edit_pie', views.edit_pie),
    path('derby', views.derby),
    path('vote/<int:id>', views.vote),
    path('do_like', views.do_like),
    path('dis_like', views.dislike),
    path('delete/<int:id>', views.delete),


    path('logout', views.logout),
]
