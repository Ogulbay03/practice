from django import template

from Account.models import QuizTakers

register = template.Library()


@register.filter
def is_completed(request, id):
	return QuizTakers.objects.filter(user_id=request.user.id, quiz_id=id).exists()


@register.filter
def subtract(value, arg):
	return value - arg
