"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from review import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', LoginView.as_view(
        template_name='review/signin.html',
        redirect_authenticated_user=True,
        extra_context={
            'page_name': 'Connexion',
            'menu': None
        }
    ), name='signin'),
    path('flux/', views.flux, name='flux'),
    path('posts/', views.posts, name='posts'),
    path('follow/', views.follows, name='follow'),
    path('follow-user/', views.follow_user, name='follow_user'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('logout/', LogoutView.as_view() ,name='logout'),
    path('ticket/<int:id>/', views.ticket, name='ticket'),
    path('new-ticket', views.new_ticket, name='new-ticket'),
    path('ticket-answer/<int:id>/', views.ticket_answer, name='ticket-answer'),
    path('review/<int:id>/', views.review, name='review')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)