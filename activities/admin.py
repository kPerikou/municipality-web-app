from django.contrib import admin

# Register your models here.
from activities.models import Employee, DeptDirector, OfficeClerk, Direction, Department, Office, Activity, Task, Project, Comment

admin.site.register(Employee)
admin.site.register(DeptDirector)
admin.site.register(OfficeClerk)
admin.site.register(Direction)
admin.site.register(Department)
admin.site.register(Office)
admin.site.register(Activity)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Comment)
