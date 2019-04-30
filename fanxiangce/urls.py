from django.urls import path, re_path

from . import views

app_name = 'fanxiangce'

urlpatterns = [
    # re_path(r'^aaa/(?P<num>\d)?$', views.page, name='page'),
    # path('about/', TemplateView.as_view(template_name="about.html")),
    path('', views.index, name='index'),
    path('photo/<int:photo_id>', views.photo, name='photo'),
    path('user/<str:username>', views.albums, name='albums'),
    path('album/<int:album_id>', views.album, name='album'),
    path('explore', views.explore, name='explore'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('confirm/<token>', views.confirm, name='confirm'),
    path('unconfirmed', views.unconfirmed, name='unconfirmed'),
    path('resend_confirmation', views.resend_confirmation, name='resend_confirmation'),
]
