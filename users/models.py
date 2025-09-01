from django.db import models

# Create your models here.
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    events = models.ManyToManyField(
        Event,
        related_name='participants',
        blank=True
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1
    )
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # details

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(
        Task,
        on_delete=models.DO_NOTHING,
        related_name='details',
    )
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details form Task {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name
