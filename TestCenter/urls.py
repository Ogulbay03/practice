from django.contrib import admin
from django.urls import path
from Account.views import Home, login_request, register, tests, test_request, logout_request

urlpatterns = [
	path('', Home, name="home"),
	path('login/', login_request, name="login"),
	path('register/', register, name="register"),
	path('tests/', tests, name="tests"),
	path('test/<int:id>', test_request, name="test"),
	path("logout", logout_request, name="logout"),
	path('admin/', admin.site.urls),
]
