from django.contrib.auth.models import User
from django.db import models


class Test(models.Model):
	title = models.CharField(max_length=25)

	def __str__(self):
		return self.title


class Question(models.Model):
	title = models.CharField(max_length=50)
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

	def __str__(self):
		return self.title


class Answer(models.Model):
	text = models.CharField(max_length=25)
	correct = models.BooleanField(default=False)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

	def __str__(self):
		return self.text


class QuizTakers(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiztakers')
	quiz = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='takers')
	correct_answers = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username


class Response(models.Model):
	quiztaker = models.ForeignKey(QuizTakers, on_delete=models.CASCADE, related_name='responses')
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
