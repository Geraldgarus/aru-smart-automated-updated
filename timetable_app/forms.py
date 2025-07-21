from django import forms
from .models import School, Department, ProgramDegree, YearOfStudy, Course, Lecturer, Room, TimeSlot

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter School Name'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'school']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Department Name'}),
        }

    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label="----Select School----")


class ProgramDegreeForm(forms.ModelForm):
    class Meta:
        model = ProgramDegree
        fields = ['name', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Program Degree Name'}),
        }

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="----Select Department----")

class YearOfStudyForm(forms.ModelForm):
    class Meta:
        model = YearOfStudy
        fields = ['program_degree', 'year', 'total_students']
        widgets = {
            'program_degree': forms.Select(attrs={'placeholder': 'Select Program Degree'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Enter Year of Study'}),
            'total_students': forms.NumberInput(attrs={'placeholder': 'Enter Total Students'}),
        }

    program_degree = forms.ModelChoiceField(queryset=ProgramDegree.objects.all(), empty_label="----Select Program Degree----")

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'year_of_study', 'credits']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Course Name'}),
            'credits': forms.NumberInput(attrs={'placeholder': 'Enter Number of Credits'}),
        }

    year_of_study = forms.ModelChoiceField(queryset=YearOfStudy.objects.all(), empty_label="----Select Year of Study----")

class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ['name', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Lecturer Name'}),
        }

    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="----Select Course----")

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Room Name'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Enter Room Capacity'}),
        }

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['day'].choices = [('', '----Select Day of the Week----')] + self.fields['day'].choices[1:]
        
        
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
