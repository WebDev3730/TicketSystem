from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import TicketSubmissionForm, RegistrationForm, AuthenticationForm, CustomAuthenticationForm, TicketUpdateForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Ticket, User, Comment, Notification
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import random
# Create your views here.

class TicketView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'view_tickets.html'
    login_url = '/login/'
    context_object_name = 'Tickets'
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return Ticket.objects.all()
        elif user.groups.filter(name='Support').exists():
            return Ticket.objects.filter(Q(assigned_to=user) | Q(user=user))
        elif user.groups.filter(name='end-user').exists():
            return Ticket.objects.filter(Q(user=user) | Q(assigned_to=user))
        else:
            return Ticket.objects.none()
        
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'ticket_details.html'
    context_object_name = 'ticket'

    def get_func(self):
        ticket = self.get_object()
        user = self.request.user
        
        is_admin = user.groups.filter(name='Admin').exists()
        is_owner = self.request.user == user

        return is_admin or is_owner
    

    

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_group, _ = Group.objects.get_or_create(name='end-user')
            user.groups.add(default_group)
            messages.success(request, 'You Have Registered Successfully')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('view_tickets')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
        logout(request)
        return redirect('login')
   
class CreateTicketView(CreateView):
    model = Ticket
    form_class = TicketSubmissionForm
    template_name = 'add_ticket.html'
    success_url = reverse_lazy('view_tickets')

    def form_valid(self, form):
        form.instance.user = self.request.user
        support_group = Group.objects.get(name='Support')
        support_members = support_group.user_set.all()
        members_list = list(support_members)
        if support_members.exists():
            selected_support_user = random.choice(members_list)
        else:
            selected_support_user = None
        ticket = form.save(commit=False)
        ticket.assigned_to = selected_support_user
        ticket.save()
        create_notification(ticket, selected_support_user, f"A New Ticket Has Been Created: {ticket.title}")
        return super().form_valid(form)

class UpdateTicketView(UpdateView):
    model = Ticket
    template_name = 'update_ticket.html'
    form_class = TicketUpdateForm
    success_url = reverse_lazy('view_tickets')

    def form_valid(self, form):
        if self.request.user.groups.filter(name__in=['Admin', 'Support']).exists():
            form.instance.updated_by = self.request.user
            support_group = Group.objects.get(name='Support')
            support_members = support_group.user_set.all()
            members_list = list(support_members)
            if support_members.exists():
                selected_support_user = random.choice(members_list)
            else:
                selected_support_user = None
            ticket = form.save(commit=False)
            ticket.assigned_to = selected_support_user
            ticket.save()
            form.save()
            create_notification(ticket, selected_support_user, f"A Ticket Has Been Assigned To You: {ticket.title}")
            return super().form_valid(form)
        else:
            raise PermissionDenied("You don't have permission to update this ticket.")

        
class Comment(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('ticket_details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        # Inside the Comment view (after saving the comment)
        ticket = form.instance.ticket
        assigned_to_user = ticket.assigned_to  # assuming you have a 'assigned_to' field
        create_notification(ticket, assigned_to_user, f"New comment added to your ticket: {ticket.title}")

        form.save()
        return super().form_valid(form)
    
def create_notification(ticket, user, message):
    
    if ticket.assigned_to:
        Notification.objects.create(
            user=ticket.assigned_to,
            ticket=ticket,
            message=message,
    )
        send_mail(
            'Ticket Update Notification',  # Subject
            message,  # Message
            settings.DEFAULT_FROM_EMAIL,  # From email (can use your default email or set it up in settings)
            [ticket.assigned_to.email],  # Recipient email
            fail_silently=False,
            )

    if ticket.user:
        Notification.objects.create(
            user=ticket.user,
            ticket=ticket,
            message=message,
    )
        send_mail(
            'Ticket Update Notification',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.user.email],
            fail_silently=False,
        )

def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')
    context = {'notifications': notifications}
    return render(request, 'user_notifications.html', context)

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('user_notifications')

def home(request):
    return render(request, 'home.html')
