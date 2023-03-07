from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from Account.forms import NewUserForm
from Account.models import Test, QuizTakers, Response, Question, Answer


def Home(request):
	return render(request, "Home.html")


def tests(request):
	Tests = Test.objects.all()
	return render(request, "tests.html", context={"tests": Tests})


def test_request(request, id):
	exists = QuizTakers.objects.filter(user_id=request.user.id, quiz_id=id).exists()
	if request.method == 'POST' and request.user.is_authenticated and not exists:
		corrects = 0
		taker = QuizTakers.objects.create(user=request.user, quiz=Test.objects.get(id=id), correct_answers=corrects, completed=True)
		key: str
		for key, answer_id in request.POST.items():
			if not key.startswith("question_"): continue
			question_id = int(key.replace("question_", ""))
			answer = Answer.objects.get(id=answer_id)
			if answer.correct:
				corrects = corrects + 1
			print(answer.id)
			print(taker.id)
			Response.objects.create(quiztaker_id=taker.id, question_id=question_id, answer_id=answer.id)

		exists = True
		taker.correct_answers = corrects
		taker.save()

	if not exists:
		test = Test.objects.get(id=id)
		quiztaker = QuizTakers.objects.none()
		percent = 0
	else:
		test = Test.objects.none()
		quiztaker = QuizTakers.objects.filter(user_id=request.user.id, quiz_id=id).first()
		percent = (100 / quiztaker.quiz.questions.count()) * quiztaker.correct_answers

	return render(request, "test.html", context={'test': test, 'exist': exists, 'taker': quiztaker, "percent": percent})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("home")


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form": form})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="register.html", context={"form": form})
