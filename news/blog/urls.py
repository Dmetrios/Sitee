from django.urls import path, re_path

from blog.views import *

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name= 'contact'),
    path('logout', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('cats/<slug:cat>', categories),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/update', PostUpdate.as_view(), name='post_update'),
    path('post/<slug:post_slug>/delete', PostDelete.as_view(), name='post_delete'),
    path('category/<slug:cat_slug>', PostCategory.as_view(), name= 'category'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]