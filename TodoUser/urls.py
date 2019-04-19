from django.contrib import admin
from django.urls import path, include
from accounts.views import contact
from .views import home
from accounts.views import todo
from accounts.views import login_view, register_view, logout_view, download
from django.contrib.auth.views import PasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',todo),
    path('accounts/login/', login_view),
    path('accounts/register/', register_view),
    path('accounts/logout/', logout_view),
    path('accounts/contact/',contact),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/download/', download),
]
