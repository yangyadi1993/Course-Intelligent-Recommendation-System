from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea
import datetime
from django.forms.extras.widgets import SelectDateWidget

from .models import *
import re


class Registration_form(forms.Form):
    username = forms.CharField(max_length=20, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(max_length=16,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Password', 'id': 'inputEmail', 'class': 'form-control'}),
                               required=False)
    confirm_password = forms.CharField(max_length=16,
                                       widget=forms.PasswordInput(
                                           attrs={'placeholder': 'Confirm password', 'id': 'inputPasswordConfirm',
                                                  'class': 'form-control'}),
                                       required=False)
    first_name = forms.CharField(max_length=20, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=20, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))
    email = forms.CharField(max_length=255, required=False,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Email', 'id': 'inputEmail', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(Registration_form, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username or len(username) == 0:
            raise forms.ValidationError("User name is required.")
        if username and len(username) > 20 or len(username) < 6:
            raise forms.ValidationError("Username's length should be with 6 - 20.")
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already token.")
        if username and not re.match(r'^(([0-9]*)(_*)([a-zA-Z]*))*$', username):
            raise forms.ValidationError("Username contains only digits, letters and \"_\". ")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) == 0:
            raise forms.ValidationError("Password is required.")
        if password and len(password) > 16 or len(password) < 6:
            raise forms.ValidationError("Password's length should be with 6 - 16.")
        if password and not re.match(r'^(([0-9]*)(_*)([a-z]*))*$', password):
            raise forms.ValidationError("Password contains only digits, letters and \"_\". ")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password or len(confirm_password) == 0:
            raise forms.ValidationError("Please confirm your password.")

        if password and confirm_password and str(password) != str(confirm_password):
            raise forms.ValidationError("Passwords did not match. Please retype your passwords.")
        return confirm_password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or len(first_name) == 0:
            raise forms.ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or len(last_name) == 0:
            raise forms.ValidationError("Last name is required.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or len(email) == 0:
            raise forms.ValidationError("Email address is required.")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already token.")
        return email


class Change_password_form(forms.Form):
    password = forms.CharField(max_length=16,
                               label='Password',
                               widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(max_length=16,
                                       label='Confirm password',
                                       widget=forms.PasswordInput(), required=False)

    def clean(self):
        cleaned_data = super(Change_password_form, self).clean()
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) == 0:
            raise forms.ValidationError("Password is required.")
        if password and len(password) > 16 or len(password) < 6:
            raise forms.ValidationError("Password's length should be with 6 - 16.")
        if password and not re.match(r'^(([0-9]*)(_*)([a-z]*))*$', password):
            raise forms.ValidationError("Password contains only digits, letters and \"_\". ")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password or len(confirm_password) == 0:
            raise forms.ValidationError("Please confirm your password.")

        if password and confirm_password and str(password) != str(confirm_password):
            raise forms.ValidationError("Passwords did not match. Please retype your passwords.")
        return confirm_password


class User_profile_form(forms.ModelForm):
    class Meta:
        model = User_profile
        exclude = ('user', 'picture', 'resume')
        fields = ['phone', 'summary', 'location', 'industry']

    def clean(self):
        cleaned_data = super(User_profile_form, self).clean()
        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[0-9]{10}$', phone):
            raise forms.ValidationError("Phone number format error. Please input a valid phone number.")
        return phone


class Education_form(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'major', 'minor', 'start_date', 'graduate_date']

    def clean(self):
        cleaned_data = super(Education_form, self).clean()
        return cleaned_data

    def clean_school_name(self):
        school_name = self.cleaned_data.get('school_name')
        if not school_name or len(school_name) == 0:
            raise forms.ValidationError("School name is required.")
        return school_name

    def clean_degree(self):
        degree = self.cleaned_data.get('degree')
        if not degree or len(degree) == 0:
            raise forms.ValidationError("Degree is required.")
        return degree

    def clean_major(self):
        major = self.cleaned_data.get('major')
        if not major or len(major) == 0:
            raise forms.ValidationError("Major is required.")
        return major

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("Start date is required.")
        return start_date

    def clean_graduate_date(self):
        graduate_date = self.cleaned_data.get('graduate_date')
        if not graduate_date:
            raise forms.ValidationError("Graduate date is required.")
        return graduate_date

    def start_date_graduate_date(self):
        start_date = self.cleaned_data.get('start_date')
        graduate_date = self.cleaned_data.get('graduate_date')
        if graduate_date < start_date:
            raise forms.ValidationError("Graduate date should be later than start date.")
        return graduate_date


class Project_form(forms.ModelForm):
    class Meta:
        model = Academic_project
        fields = ['project_name', 'organization_name', 'responsibility', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super(Project_form, self).clean()
        return cleaned_data

    def clean_project_name(self):
        project_name = self.cleaned_data.get('project_name')
        if not project_name or len(project_name) == 0:
            raise forms.ValidationError("Project name is required.")
        return project_name

    def clean_organization_name(self):
        organization_name = self.cleaned_data.get('organization_name')
        if not organization_name or len(organization_name) == 0:
            raise forms.ValidationError("Organization name is required.")
        return organization_name

    def clean_responsibility(self):
        responsibility = self.cleaned_data.get('responsibility')
        if not responsibility or len(responsibility) == 0:
            raise forms.ValidationError("Responsibility is required.")
        return responsibility

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description) == 0:
            raise forms.ValidationError("Description is required.")
        return description

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("Start date is required.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if not end_date:
            raise forms.ValidationError("End date is required.")
        return end_date

    def start_date_graduate_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError("End date should be later than start date.")
        return end_date


class Work_experience_form(forms.ModelForm):
    class Meta:
        model = Work_experience
        fields = ['employer_name', 'location_city', 'location_country', 'responsibility',
                  'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super(Work_experience_form, self).clean()
        return cleaned_data

    def clean_organization_name(self):
        employer_name = self.cleaned_data.get('employer_name')
        if not employer_name or len(employer_name) == 0:
            raise forms.ValidationError("Organization name is required.")
        return employer_name

    def clean_location_city(self):
        location_city = self.cleaned_data.get('location_city')
        if not location_city or len(location_city) == 0:
            raise forms.ValidationError("City is required.")
        return location_city

    def clean_location_country(self):
        location_country = self.cleaned_data.get('location_country')
        if not location_country or len(location_country) == 0:
            raise forms.ValidationError("Country is required.")
        return location_country

    def clean_responsibility(self):
        responsibility = self.cleaned_data.get('responsibility')
        if not responsibility or len(responsibility) == 0:
            raise forms.ValidationError("Responsibility is required.")
        return responsibility

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("Start date is required.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if not end_date:
            raise forms.ValidationError("End date is required.")
        return end_date

    def start_date_graduate_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError("End date should be later than start date.")
        return end_date


class Honor_form(forms.ModelForm):
    class Meta:
        model = Honor
        fields = ['title', 'issued_organization', 'issued_date']

    def clean(self):
        cleaned_data = super(Honor_form, self).clean()
        return cleaned_data

    def clean_issued_organization(self):
        issued_organization = self.cleaned_data.get('issued_organization')
        if not issued_organization or len(issued_organization) == 0:
            raise forms.ValidationError("Organization name is required.")
        return issued_organization

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title) == 0:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_issued_date(self):
        issued_date = self.cleaned_data.get('issued_date')
        if not issued_date:
            raise forms.ValidationError("Issued date is required.")
        return issued_date


class Skill_set_form(forms.ModelForm):
    class Meta:
        model = Skill_set
        fields = ['skill_name', 'proficiency']

    def clean(self):
        cleaned_data = super(Skill_set_form, self).clean()
        return cleaned_data

    def clean_skill_name(self):
        skill_name = self.cleaned_data.get('skill_name')
        if not skill_name or len(skill_name) == 0:
            raise forms.ValidationError("Skill is required.")
        return skill_name

    def clean_proficiency(self):
        proficiency = self.cleaned_data.get('proficiency')
        if not proficiency or len(proficiency) == 0:
            raise forms.ValidationError("Proficiency is required.")
        return proficiency


class Language_set_form(forms.ModelForm):
    class Meta:
        model = Language_set
        fields = ['language_name', 'proficiency']

    def clean(self):
        cleaned_data = super(Language_set_form, self).clean()
        return cleaned_data

    def clean_language_name(self):
        language_name = self.cleaned_data.get('language_name')
        if not language_name or len(language_name) == 0:
            raise forms.ValidationError("Language is required.")
        return language_name

    def clean_proficiency(self):
        proficiency = self.cleaned_data.get('proficiency')
        if not proficiency or len(proficiency) == 0:
            raise forms.ValidationError("Proficiency is required.")
        return proficiency


class Achievement_form(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ('user', 'course',)
        widgets = {
            'comment': forms.Textarea(),
            'start_date': forms.TextInput(attrs={'id': 'datepicker'}),
            'end_date': forms.TextInput(attrs={'id': 'datepick'}),
        }

    def clean(self):
        cleaned_data = super(Achievement_form, self).clean()
        return cleaned_data

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('start_date')
        if end_date < start_date:
            raise forms.ValidationError("End date must be later than start date.")
        return end_date

    def start_date_graduate_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date > start_date:
            raise forms.ValidationError("End date should be later than start date.")
        return end_date


class File_form(forms.ModelForm):
    class Meta:
        model = ModelFile
        exclude = ('user',)
        widget = {'file': forms.FileInput()}

    def clean(self):
        cleaned_data = super(File_form, self).clean()
        return cleaned_data
