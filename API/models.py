from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django.contrib.auth.models import User
from API.data import GENDER_CHOICES



#pk mail, name, nick_name, birthdate (dd/mm/yyyy), psw, gender

class UserProfile(models.Model):

	""" Represents a user profile (only app user)
	In user auth.User is used for common general User fields (username, name, email, password, is_staff, is_superuser, date_joinde)
	"""

	user = models.OneToOneField(
		'auth.User',
		verbose_name = u'Cuenta de usuario',
	)

	gender = models.PositiveSmallIntegerField(
		choices = GENDER_CHOICES,
		verbose_name = u'Genero',
		null = False,
		blank = False,
	)

	nick_name = models.CharField(
		max_length = 40,
		verbose_name = u'Apodo',
		blank = True,
		null = True,
	)

	birthdate = models.DateField(
		verbose_name = u'Fecha de nacimiento',
		blank = True,
		null = True,
	)

	terms_conditions_accepted = models.BooleanField(
		default = False,
		verbose_name = u'Acepta terminos y condiciones'
	)


class Activities(models.Model):

	"""Represents the activities available to complete
	in the Mobile app
	"""

	activity_name = models.CharField(
		verbose_name = u'Actividad',
		max_length = 40,
		null = False,
		blank = False,
	)

class ActivitiesRealized(models.Model):

	"""Representes the activities completed by the app users
	"""

	user = models.ForeignKey(
		'API.UserProfile',
		null = False,
		blank = False,
		verbose_name = u'Usuario ejecutor',
	)

	activity_executed = models.ForeignKey(
		'API.Activities',
		null = False,
		blank = False,
		verbose_name = u'Actividad ejecutada',
	)

	execution_state = models.BooleanField(
		default = False,
		verbose_name = u'Se ejecuto la actividad'
	)








