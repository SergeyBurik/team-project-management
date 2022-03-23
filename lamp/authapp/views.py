from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse


def join(request):
	if request.method == 'POST':
		username = request.POST['username']
		name = request.POST['name']
		surname = request.POST['surname']
		email = request.POST['email']
		password = request.POST['password']

		# saving user to db
		User.objects.create_user(
			username, email, password,
			first_name=name, last_name=surname
		)

		# auto login
		user = auth.authenticate(username=username, password=password)
		auth.login(request, user)
		return redirect(reverse('main:boards', kwargs={"user": username}))
	else:
		return render(request, 'authapp/join.html')


def login(request):
	print(request.user.is_authenticated)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
			return redirect(reverse('main:main'))

	return render(request, 'authapp/login.html')


def logout(request):
	auth.logout(request)
	return redirect('/')