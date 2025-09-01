from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employe,Task
from tasks.forms import TaskModelForm 

# Create your views here.
def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")
def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")
def test(request):
    return render(request,'test.html')

def create_task(request):
    employees=Employe.objects.all()
    form=TaskModelForm(employees=employees)
    if request.method =="POST":
        form=TaskModelForm(request.POST,employees=employees)
        if form.is_valid():
            form.save()
            return render(request,'task_form.html',{"form":form,"message":"task sucessfull"})
    context={
        "form": form
    }
    return render(request,'task_form.html',context)

def view_task(request):
    tasks=Task.objects.filter(title__icontains="c",status="PENDING")
    return render(request, "show_task.html", {"tasks": tasks,})




from django.utils import timezone
from django.db.models import Count
from .models import  Project, TaskDetailss

def task_queries_view(request):
    employee_id = 1  
    project_id = 1   

    today = timezone.now().date()
    week_ago = today - timezone.timedelta(days=7)

    queries = {
        "tasks_for_employee": TaskDetailss.objects.filter(assigned_to__id=employee_id),
        "employees_for_project": Employe.objects.filter(taskdetailss__project__id=project_id).distinct(),
        "tasks_due_today": TaskDetailss.objects.filter(due_date=today),
        "tasks_priority_high": TaskDetailss.objects.exclude(priority='low'),
        "completed_tasks_count": TaskDetailss.objects.filter(assigned_to__id=employee_id, status='completed').count(),
        "most_recent_task": TaskDetailss.objects.latest('assigned_date'),
        "projects_without_tasks": Project.objects.filter(taskdetailss__isnull=True),
        "overdue_tasks": TaskDetailss.objects.filter(due_date__lt=week_ago, status__in=['pending', 'in-progress']),
        "task_count_per_employee": Employe.objects.annotate(task_count=Count('taskdetailss')),
        "tasks_completed_or_in_progress": TaskDetailss.objects.filter(status__in=['completed', 'in-progress']),
    }

    return render(request, "task_queries.html", {"queries": queries})
