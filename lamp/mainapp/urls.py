from django.urls import path
from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    path('<str:user>/boards/', views.boards, name='boards'),
    path('', views.main, name='main'),
    path('<str:board>/invite/', views.invite, name='invite'),
    path('<str:user>/<int:board>/', views.board, name='board'),
    path('<int:column>/task/', views.create_task, name='create_task'),
    path('<str:user>/board/<int:board>/column/create/', views.create_column, name='create_column')
]
