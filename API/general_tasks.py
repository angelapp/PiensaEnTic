from API.models import ActivitiesRealized, UserProfile, Activities 
from API.serializers import ActivitiesExecutedSerializers

def generate_activities_register(user_profile, activity_register_list):

	"""
		Function used to register a list of activities realized by a user
		If the user has a register for the ActivitiesRealized, it only updates the execution_state field,
		else, create a new ActivitiesRealized register
	"""

	for activity in activity_register_list:

		serializer = ActivitiesExecutedSerializers(data = activity)

		serializer.is_valid(raise_exception = True)

		activity_executed_name = serializer.validated_data['activity_executed']
		execution_state = serializer.validated_data['execution_state']
		user = user_profile
		try:
			activity_instance = Activities.objects.get(activity_name = activity_executed_name)
		except :
			activity_instance = Activities.objects.create(
				activity_name = activity_executed_name,
			)
		
		try:
			activity_realized_by_user = ActivitiesRealized.objects.get(
				activity_executed = activity_instance,
				user = user_profile
			)
			activity_realized_by_user.execution_state = execution_state
			activity_realized_by_user.save()
		except:
			activity_executed = ActivitiesRealized.objects.create(
				user = user_profile,
				activity_executed = activity_instance,
				execution_state = execution_state,
			)

		#activity_executed.save()








