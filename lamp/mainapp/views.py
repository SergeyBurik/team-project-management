from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.middleware import csrf
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import mainapp.utils as utils
from mainapp.models import Board, Teammate, Column, Task


# GET /
def main(request):
	if request.user.is_authenticated:
		return redirect(reverse('main:boards', kwargs={'user': request.user.username}))
	else:
		return render(request, 'mainapp/main.html')


# GET <str:user>/boards/
@login_required(login_url='/auth/login/')
def boards(request, user):
	# get user
	user = User.objects.get(username=user)
	if user == request.user:
		# get boards
		boards_ = Board.objects.filter(author=user)

		# get teammates boards
		teammate_boards = Teammate.objects.filter(user=request.user)

		return render(request, 'mainapp/boards.html', {
			'boards': boards_,
			'teammate_boards': teammate_boards,
			'user': user,
			"csrf": csrf.get_token(request),
			'board_types': Board.CATEGORIES
		})
	else:
		return HttpResponseForbidden()


# GET <str:board>/invite/
@login_required(login_url="/auth/login/")
def invite(request, board):
	# get board
	board_ = get_object_or_404(Board, token=board)

	# create new teammate
	if not len(Teammate.objects.filter(board=board_, user=request.user)):
		Teammate.objects.create(board=board_, user=request.user)

	return redirect(
		reverse('main:boards', kwargs={'user': request.user})
	)


# GET <str:user>/board/<int:board>/column/create/
def create_column(request, user, board):
	# get board
	board = get_object_or_404(Board, id=board)
	if request.method == "POST":
		# create new column
		Column.objects.create(name=request.POST.get("name", ""), board=board)

	return HttpResponseRedirect(
		reverse(
			"main:board",
			kwargs={"user": board.author.username, "board": board.id}
		)
	)


# POST <int:column>/task/
def create_task(request, column):
	# get board column
	col = get_object_or_404(Column, id=column)

	if request.method == "POST":
		# create task
		Task.objects.create(
			name=request.POST.get("name", ""),
			description="",
			column=col
		)

		return HttpResponseRedirect(
			reverse(
				"main:board",
				kwargs={"user": col.board.author.username, "board": col.board.id}
			)
		)


# GET <str:user>/<int:board>/
def board(request, user, board):
	# get the board
	board_ = get_object_or_404(Board, author__username=user, id=board)

	# find all teammates of the board
	teammates = Teammate.objects.filter(board=board_)
	# if user is not the board owner or teammate
	if not (request.user == board_.author or
			utils.in_list(request.user, [user.user for user in teammates])):
		return HttpResponseForbidden()

	# format data
	data = []
	for column in Column.objects.filter(board=board_):
		data.append({"id": column.id, "name": column.name, "tasks": Task.objects.filter(column=column)})

	return render(request, 'mainapp/board.html', {
		'board': board_, 'data': data, 'users': teammates
	})
