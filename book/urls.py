from django.urls import path
from .views import *


urlpatterns = [
    path('', BooksHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpost/', AddPost.as_view(), name='add_post'),
    path('contact/', contact, name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),

    path('logout/', logout_user, name='logout'),

    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),
]


