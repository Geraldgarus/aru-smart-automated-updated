from django.contrib import admin
from .models import School, Department, ProgramDegree, YearOfStudy, Course, Lecturer, Room, TimeSlot, Timetable

# Register your models here
admin.site.register(School)
admin.site.register(Department)
admin.site.register(ProgramDegree)
admin.site.register(YearOfStudy)
admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(Timetable)
