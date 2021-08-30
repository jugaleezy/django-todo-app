from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.

class AppLogin(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')


class SignupPage(FormView):
    template_name = 'todoapp/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupPage, self).form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(SignupPage, self).get(request, *args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(user=self.request.user).count()

        search_input = self.request.GET.get('search-data') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)
        context['search_input'] = search_input

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'status', 'category']
    success_url = reverse_lazy('tasks')
    template_name = 'todoapp/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'status', 'category']
    success_url = reverse_lazy('tasks')
    template_name = 'todoapp/task_create.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = ['title']
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'todoapp/task_delete.html'

