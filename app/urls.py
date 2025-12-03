# app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'app'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('commit', views.CommitView.as_view(), name='commit'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register')
    path('search/', views.SearchView.as_view(), name='search'),  # 添加搜索路由
]