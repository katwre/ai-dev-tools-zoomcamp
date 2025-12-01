from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Todo
from django.utils.timezone import now

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def todo_detail(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    return render(request, 'todo_detail.html', {'todo': todo})

def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Todo.objects.create(title=title, description=description, due_date=due_date, is_resolved=False)
        return redirect('todo_list')
    return render(request, 'todo_form.html')

def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.due_date = request.POST.get('due_date')
        todo.is_resolved = 'is_resolved' in request.POST
        todo.save()
        return redirect('todo_list')
    return render(request, 'todo_form.html', {'todo': todo})

def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo_confirm_delete.html', {'todo': todo})
