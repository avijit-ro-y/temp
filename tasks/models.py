from django.db import models

# Create your models here.

class Employe(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField(unique=True,max_length=254)
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICE=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Process'),
        ('COMPLETED','Completed')
    ]
    project=models.ForeignKey("Project", on_delete=models.CASCADE,null=True,blank=True)
    assigned_to=models.ManyToManyField(Employe)
    title = models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(choices=STATUS_CHOICE,default='Pending', max_length=50)
    is_completed=models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDetailss(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    std_id=models.CharField(primary_key=True, max_length=50)
    task = models.OneToOneField('Task', on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)

    def __str__(self):
        return f"Details {self.task.title}"

class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    start_date=models.DateField()

    def __str__(self):
        return self.name