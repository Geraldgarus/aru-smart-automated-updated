from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SchoolForm, DepartmentForm, ProgramDegreeForm, YearOfStudyForm, CourseForm, LecturerForm, RoomForm, TimeSlotForm
from .models import School, Department, ProgramDegree, YearOfStudy, Course, Lecturer, Room, TimeSlot
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .models import School, Timetable, Room
import random
from datetime import time
from datetime import datetime, timedelta, time
import random
from django.contrib import messages
from django.shortcuts import render
from .models import Timetable, School, Room
from .models import Room

from django.shortcuts import render, get_object_or_404
from .models import ProgramDegree, YearOfStudy, Timetable, Room
from collections import defaultdict

from collections import defaultdict
from datetime import datetime

from datetime import timedelta

from datetime import timedelta

from datetime import timedelta, datetime, time

from .models import (
    School, Department, ProgramDegree,
    YearOfStudy, Course, Lecturer,
    Room
)

def create_school(request):
    form = SchoolForm()
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            if School.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "School already exists!")
            else:
                form.save()
                messages.success(request, "School saved successfully!")
            return redirect('create_school')
    return render(request, 'create_school.html', {'form': form})

def create_department(request):
    form = DepartmentForm()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            if Department.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "Department already exists!")
            else:
                form.save()
                messages.success(request, "Department added successfully!")
            return redirect('create_department')
    return render(request, 'create_department.html', {'form': form})

def create_program_degree(request):
    form = ProgramDegreeForm()
    if request.method == 'POST':
        form = ProgramDegreeForm(request.POST)
        if form.is_valid():
            if ProgramDegree.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "Program Degree already exists!")
            else:
                form.save()
                messages.success(request, "Program Degree added successfully!")
            return redirect('create_program_degree')
    return render(request, 'create_program_degree.html', {'form': form})

def create_year_of_study(request):
    form = YearOfStudyForm()
    if request.method == 'POST':
        form = YearOfStudyForm(request.POST)
        if form.is_valid():
            if YearOfStudy.objects.filter(year=form.cleaned_data['year'],
                                          program_degree=form.cleaned_data['program_degree']).exists():
                messages.error(request, "Year of Study already exists!")
            else:
                form.save()
                messages.success(request, "Year of Study added successfully!")
            return redirect('create_year_of_study')
    return render(request, 'create_year_of_study.html', {'form': form})

def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            if Course.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "Course already exists!")
            else:
                form.save()
                messages.success(request, "Course saved successfully!")
            return redirect('create_course')
    return render(request, 'create_course.html', {'form': form})

def create_lecturer(request):
    form = LecturerForm()
    if request.method == 'POST':
        form = LecturerForm(request.POST)
        if form.is_valid():
            if Lecturer.objects.filter(name=form.cleaned_data['name'],
                                       course=form.cleaned_data['course']).exists():
                messages.error(request, "Lecturer already exists for this course!")
            else:
                form.save()
                messages.success(request, "Lecturer added successfully!")
            return redirect('create_lecturer')
    return render(request, 'create_lecturer.html', {'form': form})

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            if Room.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "Room already exists!")
            else:
                form.save()
                messages.success(request, "Room added successfully!")
            return redirect('create_room')
    return render(request, 'create_room.html', {'form': form})


#forms link
def forms_link(request):
    return render(request, 'forms_link.html')


from datetime import time
import random
from django.shortcuts import render
from .models import Timetable, School, Room  # Make sure to import your models correctly


# simulated annealing aligorithms

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIME_SLOTS = [(time(h, 0), time(h + 1, 0)) for h in range(7, 20)]  # 07:00 to 21:00

# Add minutes to a time
def add_minutes(t, mins):
    full_datetime = datetime.combine(datetime.today(), t)
    new_datetime = full_datetime + timedelta(minutes=mins)
    return new_datetime.time()

# Check if two time intervals overlap with buffer
def times_overlap(start1, end1, start2, end2, gap_minutes=10):
    end1_extended = add_minutes(end1, gap_minutes)
    start2_early = add_minutes(start2, -gap_minutes)
    return start1 < end2 and start2 < end1_extended

# Check lecturer or year conflict (for time overlap)
def is_time_conflict(timetable_items, day, start, end, lecturer, year):
    for entry in timetable_items:
        if entry.day != day:
            continue
        if (entry.lecturer == lecturer or (year and entry.year_of_study == year)) and times_overlap(
            entry.start_time, entry.end_time, start, end
        ):
            return True
    return False

# Check room conflict
def is_room_conflict(timetable_items, day, start, end, room):
    for entry in timetable_items:
        if entry.day == day and entry.room == room.name and times_overlap(
            entry.start_time, entry.end_time, start, end
        ):
            return True
    return False

# Generate timetable 
def generate_and_display_timetable(request):
    timetable_entries = []
    skipped_courses = []

    Timetable.objects.all().delete()
    all_rooms = list(Room.objects.all())

    for school in School.objects.all():
        for department in school.departments.all():
            programs = department.program_degrees.all()
            if not programs:
                skipped_courses.append(("N/A", "N/A", department.name, 'No program degrees'))
                continue

            for program in programs:
                years = program.years_of_study.all()
                if not years:
                    skipped_courses.append(("N/A", "N/A", program.name, 'No years of study'))
                    continue

                for year in years:
                    courses = sorted(year.courses.all(), key=lambda c: (-c.credits, len(c.lecturers.all())))
                    if not courses:
                        skipped_courses.append(("N/A", year.year, program.name, 'No courses in year'))
                        continue

                    for course in courses:
                        lecturers = list(course.lecturers.all())
                        if not lecturers:
                            skipped_courses.append((course.name, year.year, program.name, 'No lecturers assigned'))
                            continue

                        suitable_rooms = [r for r in all_rooms if r.capacity >= year.total_students]
                        if not suitable_rooms:
                            skipped_courses.append((course.name, year.year, program.name, 'No room with enough capacity'))
                            continue

                        lecturer = random.choice(lecturers)
                        total_hours = 3 if course.credits < 10 else 4
                        hour_splits = [2, 1] if total_hours == 3 else [2, 2]

                        success = True
                        for hours in hour_splits:
                            scheduled = False
                            attempts = 0
                            max_attempts = 20000

                            day_list = DAYS[:]
                            random.shuffle(day_list)
                            hour_list = list(range(7, 21 - hours + 1))
                            random.shuffle(hour_list)

                           
                            while not scheduled and attempts < max_attempts:
                                for day in day_list:
                                    for start_hour in hour_list:
                                        start_time = time(start_hour, 0)
                                        end_time = time(start_hour + hours, 0)

                                        if is_time_conflict(timetable_entries, day, start_time, end_time, lecturer.name, year.year):
                                            continue

                                        available_rooms = [
                                            r for r in suitable_rooms
                                            if not is_room_conflict(timetable_entries, day, start_time, end_time, r)
                                        ]

                                        if available_rooms:
                                            room = random.choice(available_rooms)
                                            entry = Timetable(
                                                school=school.name,
                                                department=department.name,
                                                program_degree=program.name,
                                                year_of_study=year.year,
                                                course=course.name,
                                                lecturer=lecturer.name,
                                                day=day,
                                                start_time=start_time,
                                                end_time=end_time,
                                                room=room.name
                                            )
                                            timetable_entries.append(entry)
                                            scheduled = True
                                            break
                                    if scheduled:
                                        break
                                attempts += 1

                            # 🔁 Final fallback: 
                            if not scheduled:
                                for fallback_day in DAYS:
                                    for hour in range(7, 20):
                                        fallback_start = time(hour, 0)
                                        fallback_end = time(hour + hours, 0)

                                        if is_time_conflict(timetable_entries, fallback_day, fallback_start, fallback_end, lecturer.name, None):
                                            continue

                                        available_rooms = [
                                            r for r in suitable_rooms
                                            if not is_room_conflict(timetable_entries, fallback_day, fallback_start, fallback_end, r)
                                        ]

                                        if available_rooms:
                                            room = available_rooms[0]
                                            entry = Timetable(
                                                school=school.name,
                                                department=department.name,
                                                program_degree=program.name,
                                                year_of_study=year.year,
                                                course=course.name,
                                                lecturer=lecturer.name,
                                                day=fallback_day,
                                                start_time=fallback_start,
                                                end_time=fallback_end,
                                                room=room.name
                                            )
                                            timetable_entries.append(entry)
                                            scheduled = True
                                            print(f"✅ Scheduled in relaxed mode: {course.name}")
                                            break
                                    if scheduled:
                                        break

                            if not scheduled:
                                success = False
                                break

                        if not success:
                            skipped_courses.append((course.name, year.year, program.name, 'Scheduling failed even in relaxed mode'))

    # Save all entries
    Timetable.objects.bulk_create(timetable_entries)

    # Prepare context
    timetable_data = Timetable.objects.all().order_by(
        'school', 'department', 'program_degree', 'year_of_study', 'day', 'start_time'
    )

    room_capacity_map = {room.name: room.capacity for room in all_rooms}
    total_students_map = {}
    for school in School.objects.all():
        for department in school.departments.all():
            for program in department.program_degrees.all():
                for year in program.years_of_study.all():
                    total_students_map[(program.name, year.year)] = year.total_students

    context = {
        'timetable_data': timetable_data,
        'room_capacity_map': room_capacity_map,
        'total_students_map': total_students_map,
        'skipped_courses': skipped_courses,
    }

    request.session['skipped_courses'] = skipped_courses
    messages.success(request, "Timetable generated successfully!")
    return render(request, 'forms_link.html', context)



from django.shortcuts import render
from .models import Timetable, School, Department, ProgramDegree, Lecturer, Room




def build_timetable_cells(entries, start_hour=7, end_hour=20):
    """
    entries: list of timetable entries sorted by start_time for a day
    Class duration = 60 minutes
    Gap duration = 10 minutes between classes
    Returns list of cells (class or empty) with correct colspan
    """
    CLASS_LENGTH = 60  # class duration in minutes
    GAP_LENGTH = 10    # gap duration in minutes

    # Convert start and end hour to minutes from midnight
    current_time_mins = start_hour * 60
    end_time_mins = end_hour * 60

    cells = []

    for entry in entries:
        entry_start_mins = entry.start_time.hour * 60 + entry.start_time.minute
        entry_end_mins = entry.end_time.hour * 60 + entry.end_time.minute

        # Add empty slots until next class start, in 70-min blocks (class + gap)
        while current_time_mins + CLASS_LENGTH <= entry_start_mins:
            # Add empty slot representing 60 min class block
            cells.append({'type': 'empty', 'colspan': 1})
            current_time_mins += CLASS_LENGTH + GAP_LENGTH  # move time by 70 mins (class + gap)

        # Calculate class duration in minutes
        duration_mins = entry_end_mins - entry_start_mins

        # Calculate how many 70-min slots are needed to cover this class duration + gaps
        # We assume classes start at the beginning of a 70-min block (class + gap)
        slots = (duration_mins + GAP_LENGTH + CLASS_LENGTH - 1) // (CLASS_LENGTH + GAP_LENGTH)

        cells.append({'type': 'class', 'entry': entry, 'colspan': slots})

        # Move current time after class + gap
        current_time_mins = entry_start_mins + slots * (CLASS_LENGTH + GAP_LENGTH)

    # Fill remaining empty slots till end of day
    while current_time_mins + CLASS_LENGTH <= end_time_mins:
        cells.append({'type': 'empty', 'colspan': 1})
        current_time_mins += CLASS_LENGTH + GAP_LENGTH

    return cells

#timetable for year of study

def timetable_for_year(request, program_degree_id, year_of_study):
    program = get_object_or_404(ProgramDegree, id=program_degree_id)
    timetable_qs = Timetable.objects.filter(
        program_degree=program.name,
        year_of_study=year_of_study
    ).order_by('day', 'start_time')

    year_obj = get_object_or_404(YearOfStudy, program_degree=program, year=year_of_study)
    room_capacity_map = {room.name: room.capacity for room in Room.objects.all()}

    hours = list(range(7, 21))  # 7:00 to 20:00

    # Group timetable entries by day
    from collections import defaultdict
    day_entries = defaultdict(list)
    for entry in timetable_qs:
        day_entries[entry.day].append(entry)

    # Sort entries per day
    for day in day_entries:
        day_entries[day].sort(key=lambda e: e.start_time)

    # Build timetable cells per day
    day_cells_map = {}
    for day, entries in day_entries.items():
        day_cells_map[day] = build_timetable_cells(entries, hours)

    days = sorted(day_cells_map.keys())

    context = {
        'program_degree': program,
        'year_of_study': year_of_study,
        'total_students': year_obj.total_students,
        'room_capacity_map': room_capacity_map,
        'hours': hours,
        'days': days,
        'day_cells_map': day_cells_map,
    }

    return render(request, 'timetable_for_year.html', context)


# View to display the timetable for a specific lecturer

from collections import defaultdict

def timetable_for_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)

    timetable_qs = Timetable.objects.filter(
        lecturer=lecturer.name
    ).order_by('day', 'start_time')

    hours = list(range(7, 21))  # 07:00 to 20:00
    day_entries = defaultdict(list)

    for entry in timetable_qs:
        day_entries[entry.day].append(entry)

    for day in day_entries:
        day_entries[day].sort(key=lambda e: e.start_time)

    day_cells_map = {
        day: build_timetable_cells(entries, hours)
        for day, entries in day_entries.items()
    }

    days = sorted(day_cells_map.keys())

    context = {
        'lecturer': lecturer.name,
        'hours': hours,
        'days': days,
        'day_cells_map': day_cells_map,
    }

    return render(request, 'timetable_for_lecturer.html', context)


# View to display the timetable for a specific room

from django.shortcuts import render
from .models import Timetable


from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import Timetable, Room

def build_timetable_cells(entries, hours_range):
    cells = []
    current_hour = hours_range[0]

    for entry in entries:
        start_hour = entry.start_time.hour
        end_hour = entry.end_time.hour
        duration = end_hour - start_hour

        while current_hour < start_hour:
            cells.append({'type': 'empty', 'colspan': 1})
            current_hour += 1

        cells.append({'type': 'class', 'entry': entry, 'colspan': duration})
        current_hour = end_hour

    while current_hour < hours_range[-1] + 1:
        cells.append({'type': 'empty', 'colspan': 1})
        current_hour += 1

    return cells

def timetable_for_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        timetable_qs = Timetable.objects.filter(room=room.name).order_by('day', 'start_time')

        hours = list(range(7, 21))  # 07:00 to 20:00

        day_entries = defaultdict(list)
        for entry in timetable_qs:
            day_entries[entry.day].append(entry)

        for day in day_entries:
            day_entries[day].sort(key=lambda e: e.start_time)

        day_cells_map = {}
        for day, entries in day_entries.items():
            day_cells_map[day] = build_timetable_cells(entries, hours)

        days = sorted(day_cells_map.keys())

        context = {
            'room': room,
            'hours': hours,
            'days': days,
            'day_cells_map': day_cells_map
        }

    except Room.DoesNotExist:
        context = {
            'error': f"No room found with ID {room_id}."
        }

    return render(request, 'timetable_for_room.html', context)

#timetable links
def timetable_links_view(request):
    schools = School.objects.prefetch_related('departments__program_degrees__years_of_study').all()
    lecturers = Lecturer.objects.all()
    rooms = Room.objects.all()

    skipped_courses = request.session.pop('skipped_courses', None)  # Get and remove skipped_courses from session

    total_room_capacity = sum(room.capacity for room in rooms)  # Calculate total capacity

    context = {
        'schools': schools,
        'lecturers': lecturers,
        'rooms': rooms,
        'skipped_courses': skipped_courses,
        'total_room_capacity': total_room_capacity,  # Pass total capacity
    }

    return render(request, 'timetable_links.html', context)






# views.py
from django.shortcuts import render
from .models import School, Department, ProgramDegree, YearOfStudy, Course, Lecturer, Room, TimeSlot

# View for listing all schools
def school_list(request):
    schools = School.objects.all()
    return render(request, 'school_list.html', {'schools': schools})

# View for listing all departments
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

# View for listing all program degrees
def program_degree_list(request):
    program_degrees = ProgramDegree.objects.all()
    return render(request, 'program_degree_list.html', {'program_degrees': program_degrees})

# View for listing all years of study
def year_of_study_list(request):
    years_of_study = YearOfStudy.objects.all()
    return render(request, 'year_of_study_list.html', {'years_of_study': years_of_study})

# View for listing all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# View for listing all lecturers
def lecturer_list(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'lecturer_list.html', {'lecturers': lecturers})

# View for listing all rooms
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


#reources view
def resources(request):
    return render(request, 'resources.html')








from django.shortcuts import render, redirect, get_object_or_404
from .models import School
from .forms import SchoolForm  # Assuming you will create a form for School

# Edit school view
def edit_school(request, id):
    school = get_object_or_404(School, id=id)
    
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect('school_list')  # Redirect to the list of schools after editing
    else:
        form = SchoolForm(instance=school)
    
    return render(request, 'edit_school.html', {'form': form, 'school': school})

def delete_school(request, id):
    school = get_object_or_404(School, id=id)
    if request.method == 'POST':
        school.delete()
        return redirect('school_list')  # Redirect to the list of schools after deleting

    # If it's not a POST request, just return an empty response.
    return redirect('school_list')




# Edit department view
def edit_department(request, id):
    # Get the department object we want to edit, or return a 404 error if not found
    department = get_object_or_404(Department, id=id)
    
    # Get all available schools for the dropdown in the form
    schools = School.objects.all()

    if request.method == 'POST':
        # Get the form data from the POST request
        name = request.POST.get('name')  # New department name
        school_id = request.POST.get('school')  # Selected school id
        
        # Fetch the selected school from the database
        school = get_object_or_404(School, id=school_id)

        # Update the department with the new data
        department.name = name
        department.school = school
        department.save()  # Save the changes to the database
        
        # After saving, redirect to the department list view (you can change the URL name)
        return redirect('department_list')

    # If the request is GET, render the form with the current department details
    return render(request, 'edit_department.html', {'department': department, 'schools': schools})
# Delete department view
def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    return redirect('department_list')



# Edit view
def edit_program_degree(request, id):
    program_degree = get_object_or_404(ProgramDegree, id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        program_degree.name = request.POST.get('name')
        department_id = request.POST.get('department')
        program_degree.department = get_object_or_404(Department, id=department_id)
        program_degree.save()
        return redirect('program_degree_list')

    return render(request, 'edit_program_degree.html', {
        'program_degree': program_degree,
        'departments': departments
    })

# Delete view (with no confirmation template)
def delete_program_degree(request, id):
    program_degree = get_object_or_404(ProgramDegree, id=id)
    program_degree.delete()
    return redirect('program_degree_list')




# Edit view
def edit_year_of_study(request, id):
    year = get_object_or_404(YearOfStudy, id=id)
    programs = ProgramDegree.objects.all()

    if request.method == 'POST':
        year.year = request.POST.get('year')
        year.total_students = request.POST.get('total_students')
        program_id = request.POST.get('program_degree')
        year.program_degree = get_object_or_404(ProgramDegree, id=program_id)
        year.save()
        return redirect('year_of_study_list')

    return render(request, 'edit_year_of_study.html', {
        'year_of_study': year,
        'program_degrees': programs
    })

# Delete view (no confirmation template)
def delete_year_of_study(request, id):
    year = get_object_or_404(YearOfStudy, id=id)
    year.delete()
    return redirect('year_of_study_list')




# List view
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# Edit view

def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    years = YearOfStudy.objects.all()
    credit_choices = Course._meta.get_field('credits').choices  # <-- Add this line

    if request.method == 'POST':
        course.name = request.POST.get('name')
        course.credits = request.POST.get('credits')
        year_id = request.POST.get('year_of_study')
        course.year_of_study = get_object_or_404(YearOfStudy, id=year_id)
        course.save()
        return redirect('course_list')

    return render(request, 'edit_course.html', {
        'course': course,
        'years_of_study': years,
        'credit_choices': credit_choices  # <-- And pass it here
    })


# Delete view
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list')






def edit_lecturer(request, id):
    lecturer = get_object_or_404(Lecturer, id=id)
    courses = Course.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        course_id = request.POST.get('course')

        if name and course_id:
            lecturer.name = name
            lecturer.course = get_object_or_404(Course, id=course_id)
            lecturer.save()
            return redirect('lecturer_list')  # Update with your actual URL name

    return render(request, 'edit_lecturer.html', {
        'lecturer': lecturer,
        'courses': courses
    })
    
def delete_lecturer(request, id):
    lecturer = get_object_or_404(Lecturer, id=id)
    lecturer.delete()
    return redirect('lecturer_list')  # Update with your actual list view name





def edit_room(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')

        if name and capacity:
            room.name = name
            room.capacity = int(capacity)
            room.save()
            return redirect('room_list')  # Make sure this matches your URL name

    return render(request, 'edit_room.html', {'room': room})

def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('room_list')  # Ensure this URL name matches your list view






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed due to invalid data. Please correct and resubmit.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('forms_link')  # redirected page should show this message
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')




def index(request):
    return render(request, 'index.html')



def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # You can process the message here, e.g., save to DB or send email
        print(f"New contact message from {name} ({email}): {message}")

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Redirect to the same page after submission

    return render(request, 'contact.html')
