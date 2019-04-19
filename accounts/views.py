from django.shortcuts import HttpResponse
import csv
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import TodoList, Category
from .forms import contactform
from django.contrib.auth import (authenticate, get_user_model, login, logout)
import datetime
from .forms import UserLoginForm, UserRegisterForm 
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)

def logout_view(request):
    logout(request)
    return redirect('/')

def todo(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()
            return redirect("/")
        if "taskDelete" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id))
                todo.delete()
    return render(request, "todo.html", {"todos": todos, "categories":categories})

def contact(request):
    form_class = contactform

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get( 'contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('/')

    return render(request, 'contact.html', { 'form': form_class })

@permission_required('admin.can_add_log_entry')
def download(request):

    items = TodoList.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="TodoList.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['title', 'content', 'created', 'due_date', 'category'])
    for obj in items:
        writer.writerow([obj.title, obj.content, obj.created, obj.due_date, obj.category])

    return response
