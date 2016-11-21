
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from django.shortcuts import get_object_or_404




class UserSerializer(serializers.Serializer):

	"""

	Class used to have the serializer structure for the user model in the register
	
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

	"""

	first_name = serializers.CharField()
	last_name = serializers.CharField(
		required = False,
		allow_blank = True,
	)
	nick_name = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField(default = 'user_doesnt_has_psw')
	gender = serializers.IntegerField(default = 3)
	birthdate = serializers.CharField(
		required = False,
	)
	terms_conditions_accepted = serializers.BooleanField(
		default = True
	)

	def validate_email(self, value):
		if User.objects.filter(email = value.lower()):
			raise serializers.ValidationError("This field must be unique")
		return value


class ActivitiesExecutedSerializers(serializers.Serializer):

	"""

	Class used to have the serializer structure for the activities executed that is contained in a list
	See views.ActivityRegister for the complete JSON required for the API

	activity_executed = CharField() the keyName for the activity
	execution_state = BooleanField()
				True  if the activity was executed by the user
				False if the activity wasn't executed by the user 
		
	"""

	activity_executed = serializers.CharField()
	execution_state = serializers.BooleanField(
		default = True ,
	)




		