from django.urls import path
from apiapp import views

app_name = "apiapp"

urlpatterns = [
	path("<str:user>/boards/", views.UserBoardsView.as_view()),
	path("task/<int:taskId>/changeColumn/", views.ChangeColumnView.as_view())
]
