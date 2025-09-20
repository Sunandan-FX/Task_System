from django.contrib import admin
from .models import Employee, Task



class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'joining_date')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'status', 'due_date', 'days_left_display')
    search_fields = ('title',)
    list_filter = ('status',)

    def days_left_display(self, obj):
        days = obj.days_left()
        if days < 0:
            return f"Overdue by {-days} days"
        return f"{days} days left"
    days_left_display.short_description = "Due In"
