
from django.urls import path
from . import views  
from .views import generate_and_display_timetable


urlpatterns = [
   
     
    path('timetable/', generate_and_display_timetable, name='generate_timetable'),
   
    path('timetable/year/<int:program_degree_id>/<int:year_of_study>/', views.timetable_for_year, name='timetable_for_year'),
    path('timetable/lecturer/<int:lecturer_id>/', views.timetable_for_lecturer, name='timetable_for_lecturer'),
    path('timetable/room/<str:room_id>/', views.timetable_for_room, name='timetable_for_room'),
    path('timetable/links/', views.timetable_links_view, name='timetable_links'),
      path('schools/', views.school_list, name='school_list'),
    path('departments/', views.department_list, name='department_list'),
    path('program_degrees/', views.program_degree_list, name='program_degree_list'),
    path('years_of_study/', views.year_of_study_list, name='year_of_study_list'),
    path('courses/', views.course_list, name='course_list'),
    path('lecturers/', views.lecturer_list, name='lecturer_list'),
    path('rooms/', views.room_list, name='room_list'),
   
     path('resources/', views.resources, name='resources'),
     path('school/<int:id>/edit/', views.edit_school, name='edit_school'),
    path('school/<int:id>/delete/', views.delete_school, name='delete_school'),
      path('department/edit/<int:id>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:id>/', views.delete_department, name='delete_department'),
    path('program-degrees/edit/<int:id>/', views.edit_program_degree, name='edit_program_degree'),
    path('program-degrees/delete/<int:id>/', views.delete_program_degree, name='delete_program_degree'),
    path('years-of-study/edit/<int:id>/', views.edit_year_of_study, name='edit_year_of_study'),
    path('years-of-study/delete/<int:id>/', views.delete_year_of_study, name='delete_year_of_study'),
     path('courses/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('lecturers/edit/<int:id>/', views.edit_lecturer, name='edit_lecturer'),
path('lecturers/delete/<int:id>/', views.delete_lecturer, name='delete_lecturer'),
path('rooms/edit/<int:id>/', views.edit_room, name='edit_room'),
path('rooms/delete/<int:id>/', views.delete_room, name='delete_room'),
 path('create/school/', views.create_school, name='create_school'),
    path('create/department/', views.create_department, name='create_department'),
    path('create/program-degree/', views.create_program_degree, name='create_program_degree'),
    path('create/year-of-study/', views.create_year_of_study, name='create_year_of_study'),
    path('create/course/', views.create_course, name='create_course'),
    path('create/lecturer/', views.create_lecturer, name='create_lecturer'),
    path('create/room/', views.create_room, name='create_room'),
   path('forms-link/', views.forms_link, name='forms_link'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('', views.index, name='index'),
     path('about/', views.about_view, name='about'),

 path('contact/', views.contact_view, name='contact'),

 
]


