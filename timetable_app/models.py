from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class ProgramDegree(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='program_degrees')

    def __str__(self):
        return f"{self.name} ({self.department.name})"
class YearOfStudy(models.Model):
    year = models.PositiveSmallIntegerField()
    program_degree = models.ForeignKey(ProgramDegree, on_delete=models.CASCADE, related_name='years_of_study')
    total_students = models.PositiveIntegerField()  # New field added

    def __str__(self):
        return f"Year {self.year} - {self.program_degree.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    year_of_study = models.ForeignKey(YearOfStudy, on_delete=models.CASCADE, related_name='courses')
    credits = models.PositiveIntegerField(choices=[(8, '8 Credits'), (10, '10 Credits'), (12, '12 Credits')], default=8)

    def __str__(self):
        return f"{self.name} (Year {self.year_of_study.year} - {self.year_of_study.program_degree.name}, {self.credits} Credits)"

class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lecturers')

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    day = models.CharField(max_length=3, choices=DAY_CHOICES)

    def __str__(self):
        return self.get_day_display()
    
class Timetable(models.Model):
    school = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    program_degree = models.CharField(max_length=100)
    year_of_study = models.PositiveSmallIntegerField()
    course = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=100)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course} - {self.day} ({self.start_time} - {self.end_time})"
