from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.department})"


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title

    def days_left(self):
        return (self.due_date - date.today()).days

    def clean(self):
        # Prevent more than 5 pending tasks per employee
        if self.status == "Pending":
            pending_count = Task.objects.filter(employee=self.employee, status="Pending")
            # If creating a new task (self.pk is None), count normally
            # If updating existing, exclude itself
            if self.pk:
                pending_count = pending_count.exclude(pk=self.pk)
            if pending_count.count() >= 5:
                raise ValidationError(f"{self.employee.name} already has 5 pending tasks.")
