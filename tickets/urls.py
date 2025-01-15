from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('add_ticket/', views.CreateTicketView.as_view(), name='add_ticket'),
    path('view_tickets/', views.TicketView.as_view(), name='view_tickets'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_details'),   
    path('update_ticket/<int:pk>/', views.UpdateTicketView.as_view(), name='update_ticket'),
    path('add_comment/<int:pk>/', views.Comment.as_view(), name='add_comment'),
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('', views.home, name="home"),
]
