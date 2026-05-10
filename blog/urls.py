from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add/', views.add_article, name='add_article'),
    path('category/<str:category>/', views.category_articles, name='category_articles'),
    path('article/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),  # ← لازم يكون قبل
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('search/', views.search_view, name='search'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)