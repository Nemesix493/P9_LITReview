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
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from review import views
from review.forms import CustomAuthenticationForm

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.flux, name='default'),
    path('signup/', views.signup, name='signup'),
    path('signin/', LoginView.as_view(
        template_name='review/signin.html',
        redirect_authenticated_user=True,
        extra_context={
            'page_name': 'Connexion',
            'menu': None
        },
        authentication_form=CustomAuthenticationForm
    ), name='signin'),
    path('flux/', views.flux, name='flux'),
    path('posts/', views.posts, name='posts'),
    path('follow/', views.follows, name='follow'),
    path('follow-user/', views.follow_user, name='follow_user'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('logout/', LogoutView.as_view() ,name='logout'),
    path('ticket/<int:id>/', views.ticket, name='ticket'),
    path('new-ticket', views.new_ticket, name='new-ticket'),
    path('update-ticket/<int:id>/', views.modify_ticket, name='modify-ticket'),
    path('ticket-answer/<int:id>/', views.ticket_answer, name='ticket-answer'),
    path('review/<int:id>/', views.review, name='review'),
    path('update-review/<int:id>/', views.modify_review, name='modify-review'),
    path('new-review/', views.new_review, name='new-review'),
    path('remove-ticket/<int:id>/', views.remove_ticket, name='remove-ticket'),
    path('remove-review/<int:id>/', views.remove_review, name='remove-review'),
]

handler404 = views.custom_404
handler403 = views.custom_403


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    def test_404(request):
        return views.custom_404(request, exception=Exception('Ici s\'affiche le message d\'erreur !'))
    urlpatterns += [path('test-404/', test_404, name='test-404')]
