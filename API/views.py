from datetime import datetime

from django.conf import settings

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import parsers, renderers
from rest_framework import serializers, exceptions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.models import User

from API.serializers import UserSerializer, ActivitiesExecutedSerializers
from API.models import UserProfile, Activities, ActivitiesRealized
from API.general_tasks import generate_activities_register



class BasePostListView(APIView):

	"""
		Class used to manage list in API post methods
	"""
	throttle_class = ()
	permissions_classes = ()

	parser_classes = (
		parsers.FormParser,
		parsers.MultiPartParser,
		parsers.JSONParser,
	)

	renderer_classes = (renderers.JSONRenderer,)


class UserViewSet(APIView):

	"""
		Class used as view to post the user register. It uses the
		serializer.UserSerializer and API.models.UserProfile model

		ROOT+/api/register-user/

		first_name = CharField() required
		last_name = CharField() not_required
		nick_name = CharField() required
		email = EmailField() required, must be unique for the user
		password = CharField() required
		gender = IntegerField() required, must be one of these values:
					1 for Male
					2 for Female
					3 for Not Defined
		birthdate = DateField() not_required  YYYY-MM-DD
		terms_conditions_accepted = BooleanField() required

		Example JSON Post:
		
		{
		  "first_name" : "example",
		  "last_name" : "sampler",
		  "nick_name" : "supersampler",
		  "email" : "example@example.com",
		  "password" : "12345",
		  "gender" : 1,
		  "birthdate" : "2009-11-05",
		  "terms_conditions_accepted" : true
		}

	"""

	def post(self, request):
		api_key = request.META.get('HTTP_APIID')

		if not api_key == settings.API_KEY:
			raise Http404

		serializer = UserSerializer(data = request.data)
		serializer.is_valid(raise_exception = True)

		first_name = serializer.validated_data['first_name']
		nick_name = serializer.validated_data['nick_name']
		email = serializer.validated_data['email']
		password = serializer.validated_data['password']
		gender = serializer.validated_data['gender']
		birthdate = serializer.validated_data['birthdate']
		terms_conditions_accepted = serializer.validated_data['terms_conditions_accepted']


		#Create the user
		user = User(
			username = email.lower(),
			first_name = first_name,
			email = email,
			date_joined = datetime.now(),
		)

		user.set_password(password)
		user.save()

		#Create the user profile

		UserProfile.objects.create(
			user = user,
			nick_name = nick_name,
			gender = gender,
			birthdate = birthdate,
			terms_conditions_accepted = terms_conditions_accepted,
		)

		new_registered_user = {
			'username' : email,
			'created' : True ,
		}

		return Response(new_registered_user)

class ActivityRegister(APIView):
	
	"""
		Class to post the Activity Register List for each user
		
		ROOT+/api/activity-register/

		user_mail = CharField() the user_mail, it has to be registered previously
		activity_executed = CharField() the keyName for the activity
		execution_state = BooleanField()
				True  if the activity was executed by the user
				False if the activity wasn't executed by the user 

		Example JSON Post:

		{
		 "user_mail" : "example@example.com",
		  "activities_register" :
		  [
		    {
		    "activity_executed" : "ACTProb1",
		    "execution_state" : false
		    },
		    {
		    "activity_executed" : "ACTProb2",
		    "execution_state" : true
		  	}
		  ]
		}

	"""

	def post(self, request):
		api_key = request.META.get('HTTP_APIID')

		if not api_key == settings.API_KEY:
			raise Http404

		username = request.data.get('user_mail')

		if not User.objects.filter(email = username.lower()):
			raise serializers.ValidationError("User not exists")

		user_account = get_object_or_404(
			User,
			email = username,
		)

		user_profile = get_object_or_404(
			UserProfile,
			user = user_account
		)

		if user_profile:
			activities_register = request.data.get('activities_register')
			if activities_register:
				generate_activities_register(
					user_profile,
					activities_register,
				)
				response = unicode('updated')
			else:
				response = unicode('no-data-to-process')


		content = {
			'updated' : response,
		}

		return Response(content)

		


class PasswordRecovery(APIView):
	
	"""
		Class to send a email with the password to the user
		
		ROOT+/api/password /recovery/

		user_mail = CharField() the user_mail, it has to be registered previously
		password = CharField() the user paswword
		
		Example JSON Post:

		{
		 "user_mail" : "example@example.com",
		 "password" : "xscfsdklfj"
		}

	"""

	def post(self, request):
		api_key = request.META.get('HTTP_APIID')

		if not api_key == settings.API_KEY:
			raise Http404

		username = request.data.get('user_mail')
		password = request.data.get('password')

		if not User.objects.filter(email = username.lower()):
			raise serializers.ValidationError("User not exists")

		user = get_object_or_404(User, email = username.lower())
		name = user.first_name 
		subject = "Piensa en TIC - Recuperacion de contrasena"
		message = u'Hola ' + name + u', tu contrasena de Piensa en TIC es ' + password 
		#message = render_to_string('API/password_recovery.html',{'key':password,'name': name})
		msg = EmailMultiAlternatives(subject,message,'info@piensaentic.co',[user.email])
		msg.attach_alternative(message,"text/html")
		msg.send()


		content = {
			'sent' : u'OK',
		}

		return Response(content)
		
		




















