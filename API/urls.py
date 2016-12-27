from django.conf.urls import url, include
from API import views
from rest_framework import renderers

urlpatterns = [
	url(r'^register-user/$', views.UserViewSet.as_view(),
		name = 'user_registration',
	),

	url(r'^activity-register/$', views.ActivityRegister.as_view(),
		name = 'activity_registration',
	),

	url(r'^password-recovery/$', views.PasswordRecovery.as_view(),
		name = 'password-recovery',
	),
]