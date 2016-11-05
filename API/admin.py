
from django.contrib import admin
from django.contrib.auth.models import User, Group
from API.models import UserProfile, Activities, ActivitiesRealized



class UserAdmin(admin.ModelAdmin):
	""" Class used to represents UserProfile in the admin
	"""
	list_display = ('user','nick_name', 'gender', 'birthdate', 'terms_conditions_accepted',)
	#list_filter = ('user', 'nick_name')


class ActivitiesAdmin(admin.ModelAdmin):
	""" Class used to represents Activities List in the admin
	"""
	list_display = ('activity_name',)

class ActivitiesRealizedAdmin(admin.ModelAdmin):
	""" Class used to represents Activities Executed in the admin
	"""
	list_display = ('user', 'activity_executed','execution_state',)


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Activities, ActivitiesAdmin)
admin.site.register(ActivitiesRealized, ActivitiesRealizedAdmin)