from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    total_count = tasks.count()
    completed_count = tasks.filter(is_completed=True).count()
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'total_count': total_count,
        'completed_count': completed_count,
    })

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('task_list')
