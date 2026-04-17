
from django.contrib import admin
from .models import Student,StudentCourse,Course

admin.site.register(Student)
from .models import Contact

admin.site.register(Contact)
admin.site.register(Course)
admin.site.register(StudentCourse)