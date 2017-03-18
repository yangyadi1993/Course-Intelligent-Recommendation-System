from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth import login, authenticate

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth import views
from django.utils.encoding import force_bytes

from mimetypes import guess_type
from operator import itemgetter

import urllib.request
import urllib
import json
import math
from itertools import chain
from .models import *
from .forms import *
from .resume_controller import *

import random
import time
from django.utils.timezone import localtime
from django.utils.formats import get_format
from django.utils.dateformat import DateFormat

current_milli_time = lambda: int(round(time.time() * 1000))


def linkedin_login(request):
    username = ''
    password = ''
    if 'email' in request.POST:
        username = request.POST['username']
    if 'password' in request.POST:
        password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return redirect('login')


def linkedin_logout(request):
    auth_logout(request)
    return redirect('/')


@login_required
def get_profile(request):  # This function triggers when user click on the profile link
    context = {}
    user = request.user
    user_profile = User_profile.objects.get(user=request.user)

    try:
        social = user.social_auth.get(provider='linkedin-oauth2')
        context['social'] = social.extra_data
    except:
        context['social'] = ''

    # get information from request.user
    education = Education.get_education_by_user(request.user)
    academic_project = Academic_project.get_academic_project_by_user(request.user)
    work_experience = Work_experience.get_work_experience_by_user(request.user)
    honor = Honor.get_honor_by_user(request.user)
    skill_set = Skill_set.get_skill_set_by_user(request.user)
    language_set = Language_set.get_language_set_by_user(request.user)

    if user_profile:
        context['user_profile'] = user_profile
    # set information into context if the profile's information is exist
    if education and len(education) != 0:
        context['education'] = education
    if academic_project and len(academic_project) != 0:
        context['academic_project'] = academic_project
    if work_experience and len(work_experience) != 0:
        context['work_experience'] = work_experience
    if honor and len(honor) != 0:
        context['honor'] = honor
    if skill_set and len(skill_set) != 0:
        context['skill_set'] = skill_set
    if language_set and len(language_set) != 0:
        context['language_set'] = language_set
    # user's profile picture
    context['picture_url'] = user_profile.picture_url
    return render(request, "profile.html", context)


def DictUpdate(list1, list2):
    for aList1 in list1:
        if aList1 not in list2:
            list2.append(aList1)
    return list2


# This function is triggered by home url when user login without linkedin account
@login_required
def home(request):
    # get_course_coursera()
    # get_course_udacity()
    context = {}
    user = request.user
    context['history'] = recommend_by_history(user)
    context['similarity'] = recommend_by_similarity(request)
    if context['history'] is not None:
        if context['similarity'] is not None:
            context['courses'] = DictUpdate(context['history'], context['similarity'])
        else:
            context['courses'] = context['history']
    else:
        if len(context['similarity']) > 0:
            context['courses'] = context['similarity']
            print(len(context['similarity']))
        else:
            context['courses'] = get_random_courses()
    context['recommend_users'] = recommendation_on_users(request)

    return render(request, "main.html", context)


# This function is triggered by home url when user login with linkedin account
@login_required
def home_linkedin(request):
    context = {}
    user = request.user
    social = user.social_auth.get(provider='linkedin-oauth2')

    access_token = social.extra_data['access_token']
    # THis is the url for linkedin api
    url = 'https://api.linkedin.com/v1/people/~:(id,num-connections,picture-url,' \
          'location,industry,public-profile-url)?format=json'
    header = {'Authorization': 'Bearer %s' % access_token}
    req = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    user_profile = json.loads(response)
    # retrieve data from linkedin
    context['social'] = social.extra_data
    context['picture_url'] = user_profile['pictureUrl']

    location = user_profile['location']['name']

    old_profile = User_profile.objects.filter(user=request.user)
    if not old_profile:
        profile = User_profile(user=request.user, location=location,
                               industry=user_profile['industry'],
                               picture_url=user_profile['pictureUrl'])
        profile.save()
    context['courses'] = recommend_by_history(user)
    context['recommend_users'] = recommendation_on_users(request)
    return render(request, "main.html", context)


def recommend_by_history(user):
    if Search_history.objects.filter(user=user).count() < 1:
        return
    search_history = Search_history.objects.get(user=user)
    search_term1 = search_history.history1

    if search_term1 is not None:
        courses1 = Course.search_course_by_name(search_term1)[:10]
        if not courses1 or len(courses1) == 0:
            # if search course by name has no result, try search course by description
            courses1 = Course.search_course_by_description(search_term1)
    search_term2 = search_history.history2
    courses2 = courses1
    if search_term2 is not None:
        courses2 = Course.search_course_by_name(search_term2)[:10]
        if not courses2 or len(courses2) == 0:
            # if search course by name has no result, try search course by description
            courses2 = Course.search_course_by_description(search_term2)

    courses = []
    for course in courses1:
        if course not in courses:
            courses.append(course)

    for course in courses2:
        if course not in courses:
            courses.append(course)

    courses = courses[:12]
    return courses


# THis function get random 6 courses from couresa and udacity
def get_random_courses():
    courses = []
    courseDict = []
    # iterate to get 6 courses
    for i in range(1, 13):
        next_index = random.randint(6197, 8258)
        while next_index in courseDict:
            next_index = random.randint(6197, 8258)
        next_courses = Course.objects.filter(id=next_index)  # All courses are download to our database
        if len(next_courses) > 0:
            next_course = next_courses[0]
            courses.append(next_course)
    return courses


class Return_Course:
    course_name = ''
    course_photo_url = ''
    course_description = ''
    course_id = ''

    def __init__(self, course_id, course_name, course_photo_url, course_description):
        self.course_id = course_id
        self.course_name = course_name
        self.course_photo_url = course_photo_url
        self.course_description = course_description


# This funciton is to get another course from coursera
def next_course(courses, course_count, visited):
    next_index = random.randint(0, course_count - 1)
    while next_index in visited:
        next_index = random.randint(0, course_count - 1)
    visited.append(next_index)
    next_element = courses[next_index]
    next_id = next_element['id']
    # search the  course on coursera
    next_url = 'https://api.coursera.org/api/courses.v1?ids=' + next_id + '&fields=name,photoUrl,description'
    next_response = urllib.request.urlopen(next_url).read().decode('utf-8')
    return_course_raw = json.loads(next_response)
    long_name = return_course_raw['elements'][0]['name']
    if len(long_name) > 40:
        short_name = str(long_name)[:40] + '...'
    else:
        short_name = long_name
    return Return_Course(return_course_raw['elements'][0]['id'],
                         short_name, return_course_raw['elements'][0]['photoUrl'],
                         return_course_raw['elements'][0]['description'])


# This function triggers when user click on one specific course
@login_required
def get_course(request, id):
    context = {}
    id = id
    # select the course by course id
    course = Course.objects.get(course_id=id)
    # get all the course comments
    comments = CourseComment.objects.filter(Course=course)
    context['comments'] = comments
    context['course'] = course

    # achievement_count is to decide whether the current user has finished the course or not
    achievement_count = Achievement.objects.filter(user=request.user, course=course).count()
    if achievement_count > 0:
        context['finished'] = 1

    return render(request, "course_profile.html", context)


# this funciton is to add the course to user's collection list
@login_required
def add_collection(request, id):
    context = {}

    course = Course.get_course_by_key(id)
    if course:
        user = request.user
        course.user.add(user)
        course.save()

    courses = Course.objects.filter(user=request.user)
    context['courses'] = courses
    return render(request, 'collectlist.html', context)


# this function is to remove the course from user's collection list
@login_required
def remove_collection(request, id):
    context = {}
    # course = Course.get_course_by_key(id)
    if Course.objects.filter(course_id=id).count() > 0:
        course = Course.get_course_by_key(id)
        user = request.user
        course.user.remove(user)
        course.save()
    courses = Course.objects.filter(user=request.user)
    context['courses'] = courses
    return render(request, 'collectlist.html', context)


# this function is triggered when user click on the collection link
@login_required
def get_collection(request):
    # courses=[]
    context = {}
    # get all the courses from collection
    courses = Course.objects.filter(user=request.user)
    context['courses'] = courses
    return render(request, 'collectlist.html', context)


# This function is to comment on specific course
@login_required
def create_coursecomment(request, id):
    # if the comment is not null
    if not 'commentArea' in request.POST or not request.POST['commentArea']:
        context = json.dumps({"message": "error"})
        return HttpResponse(context, content_type='application/json')

    course = Course.objects.get(course_id=id)
    user = request.user
    new_comment = CourseComment(text=request.POST['commentArea'], user=user, Course=course)
    new_comment.save()
    df = DateFormat(localtime(new_comment.time))
    date = df.format(get_format('DATE_FORMAT'))
    time = df.format('f a')
    timestamp = date + ", " + time
    firstname = user.first_name
    lastname = user.last_name
    userid = user.id
    # convert into json format
    context = json.dumps({"commentText": request.POST['commentArea'], "firstname": firstname, "time": timestamp,
                          "lastname": lastname, "userid": userid})
    # return json ajax
    return HttpResponse(context, content_type='application/json')


# the function is to allow user register for a new account
def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = Registration_form()
        return render(request, 'register.html', context)

    form = Registration_form(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)
    # create a user object
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['confirm_password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    # create a profile object
    profile = User_profile(user=new_user)
    new_user.is_active = False

    # save these two objects
    new_user.save()
    profile.save()

    token = default_token_generator.make_token(new_user)

    # define the email body
    email_body = """Welcome to 42. Please click the link below to verify your email address and
    complete the registration of your count:
    http://%s%s """ % (request.get_host(),
                       reverse('confirm_registration', args=(new_user.email, token)))
    # send mail
    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="yadiy@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'confirm.html', context)


# this funtion is to confirm the registration, if user clicks on the sended url, they will be redirect to home page
def confirm_registration(request, email, token):
    try:
        user = User.objects.get(email=email)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        return redirect(reverse('home'))
    except:
        return redirect(reverse('register'))


# this function is to allow users to reset their password
def password_reset(request):
    context = {}
    context['email'] = ''
    if request.method == 'GET':
        return render(request, 'password_reset_form.html', context)

    if 'email' in request.POST:
        try:
            user = User.objects.get(email=request.POST['email'])
            token = default_token_generator.make_token(user)

            email_body = """Please clicke the link below to change your password
			http://%s%s """ % (request.get_host(),
                               reverse('password_reset_email',
                                       args=(urlsafe_base64_encode(force_bytes(user.id)), token)))

            send_mail(subject="Change password",
                      message=email_body,
                      from_email="yadiy@andrew.cmu.edu",
                      recipient_list=[user.email],
                      fail_silently=False)

            return render(request, 'password_reset_done.html', context)
        except:
            return render(request, 'reset_failure.html', context)


@login_required
def get_photo(request, id):
    user = User.objects.filter(id=id)[0]
    profile = User_profile.get_user_profile_by_user(user)
    if not profile.picture:
        raise Http404
    con_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=con_type)


@login_required
def upload_avatar(request):
    context = {}
    try:
        user_profile = User_profile.get_user_profile_by_user(request.user)
        context['user_profile'] = user_profile
    except:
        return redirect(reverse('get_profile'))

    new_avatar = request.FILES.get('image')
    if not new_avatar:
        return redirect(reverse('get_profile'))

    user_profile.picture = new_avatar
    user_profile.save()
    return redirect('get_profile')


@login_required
def other_user_profile(request, id):
    context = {}

    if not id:
        return reverse(redirect('home'))

    user = User.objects.filter(id=id)[0]
    user_profile = User_profile.get_user_profile_by_user(user)

    # get information from request.user
    education = Education.get_education_by_user(user)
    academic_project = Academic_project.get_academic_project_by_user(user)
    work_experience = Work_experience.get_work_experience_by_user(user)
    honor = Honor.get_honor_by_user(user)
    skill_set = Skill_set.get_skill_set_by_user(user)
    language_set = Language_set.get_language_set_by_user(user)

    collections = Course.objects.filter(user=user)
    achievements = Achievement.objects.filter(user=user)

    context['other_user_id'] = id
    context['other_user_first_name'] = user.first_name
    context['other_user_last_name'] = user.last_name
    context['other_user_email'] = user.email

    context['user_profile'] = user_profile
    # set information into context if the profile's information is exist
    if education and len(education) != 0:
        context['education'] = education
    if academic_project and len(academic_project) != 0:
        context['academic_project'] = academic_project
    if work_experience and len(work_experience) != 0:
        context['work_experience'] = work_experience
    if honor and len(honor) != 0:
        context['honor'] = honor
    if skill_set and len(skill_set) != 0:
        context['skill_set'] = skill_set
    if language_set and len(language_set) != 0:
        context['language_set'] = language_set
    # user's profile picture
    context['picture_url'] = user_profile.picture_url

    context['collections'] = collections
    context['achievements'] = achievements

    return render(request, "profile_otheruser.html", context)


@login_required
def profile_info(request):
    context = {}
    user_profile = User_profile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    return render(request, "profile_info.html", context)


@login_required
def update_info(request):
    errors = []
    contexterror = {}
    contextall = {}
    if request.method == 'GET':
        return redirect('get_profile')

    user_profile_form = User_profile_form(request.POST)

    if not user_profile_form.is_valid():
        for field in user_profile_form.visible_fields():
            if field.errors:
                print(field.errors)
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        print(errors)
        return render(request, 'profile.html', contextall)
    old_user_profile = User_profile.get_user_profile_by_user(request.user)

    if 'email' in request.POST and request.POST['email']:
        print(request.POST['email'])
        request.user.email = request.POST['email']
        request.user.save()

    if not user_profile_form.cleaned_data['phone']:
        new_phone = old_user_profile.phone
    else:
        new_phone = user_profile_form.cleaned_data['phone']

    if not user_profile_form.cleaned_data['summary']:
        new_summary = old_user_profile.summary
    else:
        new_summary = user_profile_form.cleaned_data['summary']

    if not user_profile_form.cleaned_data['location']:
        new_location = old_user_profile.location
    else:
        new_location = user_profile_form.cleaned_data['location']

    if not user_profile_form.cleaned_data['industry']:
        new_industry = old_user_profile.industry
    else:
        new_industry = user_profile_form.cleaned_data['industry']

    User_profile.update_user_profile(
        request.user,
        new_phone,
        new_summary,
        new_location,
        new_industry
    )
    # contextall = dict(get_profileinfo(request))
    # return render(request, "profile.html", contextall)
    return HttpResponse(status=200)


@login_required
def education_load(request):
    context = {}
    context['education'] = Education.get_education_by_user(request.user)
    return render(request, "education_div.html", context)


# this function is to allow users add education to their profile
@login_required
def add_education(request):
    errors = []
    contexterror = {}
    contextall = {}
    if request.method == 'GET':
        return redirect('get_profile')

    education_form = Education_form(request.POST)

    if not education_form.is_valid():
        for field in education_form.visible_fields():
            if field.errors:
                print(field.errors)
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        print(errors)
        return render(request, 'profile.html', contextall)
        # this method is defined in education model
    Education.add_education_by_user(
        request.user,
        education_form.cleaned_data['school_name'],
        education_form.cleaned_data['degree'],
        education_form.cleaned_data['major'],
        education_form.cleaned_data['minor'],
        education_form.cleaned_data['start_date'],
        education_form.cleaned_data['graduate_date'],
    )
    # return render(request, 'profile.html', contextall)
    return HttpResponse(status=200)


@login_required
def skill_load(request):
    context = {}
    context['skill_set'] = Skill_set.get_skill_set_by_user(request.user)
    return render(request, "skill_div.html", context)


@login_required
# this function is to allow users add skill to their profile
def add_skill(request):
    errors = []
    contexterror = {}
    contextall = {}

    if request.method == 'GET':
        return redirect('get_profile')

    skill_set_form = Skill_set_form(request.POST)

    if not skill_set_form.is_valid():
        for field in skill_set_form.visible_fields():
            if field.errors:
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        return render(request, 'profile.html', contextall)
    # this method is define in skill model
    Skill_set.add_skill_by_user(
        request.user,
        skill_set_form.cleaned_data['skill_name'],
        skill_set_form.cleaned_data['proficiency'],
    )
    return HttpResponse(status=200)


@login_required
def work_experience_load(request):
    context = {}
    context['work_experience'] = Work_experience.get_work_experience_by_user(request.user)
    return render(request, "work_experience_div.html", context)


@login_required
# this function is to allow users add work experience to their profile
def add_work_experience(request):
    errors = []
    contexterror = {}
    contextall = {}

    if request.method == 'GET':
        return redirect('get_profile')

    work_experience_form = Work_experience_form(request.POST)

    if not work_experience_form.is_valid():
        for field in work_experience_form.visible_fields():
            if field.errors:
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        return render(request, 'profile.html', contextall)

    # this method is defined in work model
    Work_experience.add_work_experience_by_user(
        request.user,
        work_experience_form.cleaned_data['employer_name'],
        work_experience_form.cleaned_data['location_city'],
        work_experience_form.cleaned_data['location_country'],
        work_experience_form.cleaned_data['responsibility'],
        work_experience_form.cleaned_data['description'],
        work_experience_form.cleaned_data['start_date'],
        work_experience_form.cleaned_data['end_date'],
    )
    # contextall = dict(get_profileinfo(request))
    # return render(request, 'profile.html', contextall)
    return HttpResponse(status=200)


@login_required
def honor_load(request):
    context = {}
    context['honor'] = Honor.get_honor_by_user(request.user)
    return render(request, "honor_div.html", context)


@login_required
# this function is to allow users add honor to their profile
def add_honor(request):
    errors = []
    contexterror = {}
    contextall = {}

    if request.method == 'GET':
        return redirect('get_profile')

    honor_form = Honor_form(request.POST)

    if not honor_form.is_valid():
        for field in honor_form.visible_fields():
            if field.errors:
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        return render(request, 'profile.html', contextall)
    # this method is defined in honor model
    Honor.add_honor_by_user(
        request.user,
        honor_form.cleaned_data['title'],
        honor_form.cleaned_data['issued_organization'],
        honor_form.cleaned_data['issued_date'],
    )
    # contextall = dict(get_profileinfo(request))
    # return render(request, 'profile.html', contextall)
    return HttpResponse(status=200)


@login_required
def project_load(request):
    context = {}
    context['academic_project'] = Academic_project.get_academic_project_by_user(request.user)
    return render(request, "project_div.html", context)


@login_required
# this function is to allow users add project to their profile
def add_project(request):
    errors = []
    contexterror = {}
    contextall = {}

    if request.method == 'GET':
        return redirect('get_profile')

    project_form = Project_form(request.POST)

    if not project_form.is_valid():
        for field in project_form.visible_fields():
            if field.errors:
                print(field.errors)
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        return render(request, 'profile.html', contextall)
    # this method is defined in project model
    Academic_project.add_academic_project_by_user(
        request.user,
        project_form.cleaned_data['project_name'],
        project_form.cleaned_data['organization_name'],
        project_form.cleaned_data['responsibility'],
        project_form.cleaned_data['description'],
        project_form.cleaned_data['start_date'],
        project_form.cleaned_data['end_date'],
    )
    # contextall = dict(get_profileinfo(request))
    # return render(request, 'profile.html', contextall)
    return HttpResponse(status=200)


@login_required
def language_load(request):
    context = {}
    context['language_set'] = Language_set.get_language_set_by_user(request.user)
    return render(request, "language_div.html", context)


@login_required
# this function is to allow users add education to their profile
def add_language(request):
    errors = []
    contexterror = {}
    contextall = {}

    if request.method == 'GET':
        return redirect('get_profile')

    language_set_form = Language_set_form(request.POST)

    if not language_set_form.is_valid():
        for field in language_set_form.visible_fields():
            if field.errors:
                print(field.errors)
                errors.append(field.errors)
        contexterror['errors'] = errors
        contextall.update(contexterror)
        return render(request, 'profile.html', contextall)

    Language_set.add_language_by_user(
        request.user,
        language_set_form.cleaned_data['language_name'],
        language_set_form.cleaned_data['proficiency'],
    )
    # contextall = dict(get_profileinfo(request))
    # return render(request, 'profile.html', contextall)
    return HttpResponse(status=200)


# this function is to allow users to search course
def search(request):
    context = {}
    search_term = ''
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET['search']
    else:
        redirect(reverse('/home'))

    context['search_term'] = search_term
    # search_course_by_name function is defined in course model
    courses = Course.search_course_by_name(search_term)

    if Search_history.objects.filter(user=request.user).count() < 1:
        search_history = Search_history(user=request.user, history1=search_term)
        search_history.save()

    search_history = Search_history.objects.get(user=request.user)
    search_history.history2 = search_history.history1
    search_history.history1 = search_term
    search_history.save()
    if not courses or len(courses) == 0:
        # if search course by name has no result, try search course by description
        courses = Course.search_course_by_description(search_term)
        if not courses or len(courses) == 0:
            return render(request, "search_result.html", context)
        else:
            context['courses'] = courses
    else:
        context['courses'] = courses
    return render(request, "search_result.html", context)


def get_course_2(request, key):
    context = {}
    if not key or len(key) == 0:
        return redirect(reverse('/home'))
    course = Course.get_course_by_key(key)
    if not course:
        return redirect(reverse('/home'))
    context['course'] = course
    return render(request, "course_profile_2.html", context)


# this function is to get course from coursera
def get_course_coursera():
    start = 0
    while start < 1900:
        ids = ""
        # coursera only allowed to get 100 courses per time
        url = 'https://api.coursera.org/api/courses.v1?start=' + str(start)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        json_response = json.loads(response)
        courses = json_response['elements']
        for course in courses:
            if len(ids) == 0:
                ids = course['id']
            else:
                ids += str(',' + course['id'])
        get_course_detail_coursera(ids)
        start += 100


# this function is to get detailed information from coursera and add them to our database
def get_course_detail_coursera(ids):
    url = 'https://api.coursera.org/api/courses.v1?ids=' + ids + '&fields=name,photoUrl,description,' \
                                                                 'workload,startDate,previewLink'
    response = urllib.request.urlopen(url).read().decode('utf-8')
    json_response = json.loads(response)
    courses = json_response['elements']
    for course in courses:
        course_id = course['id']
        course_name = course['name']
        if 'workload' in course:
            workload = course['workload']
        else:
            workload = ''
        picture_url = course['photoUrl']
        if 'description' in course:
            course_description = course['description']
        else:
            course_description = ''

        if len(course_description) >= 3000:
            course_description = course_description[:2800] + "..."

        Course.add_course(course_id,
                          course_name,
                          workload,
                          picture_url,
                          course_description)


# get all course from udacity and add them to our database
def get_course_udacity():
    url = 'https://udacity.com/public-api/v0/courses'
    response = urllib.request.urlopen(url).read().decode('utf-8')
    json_response = json.loads(response)
    courses = json_response['courses']
    for course in courses:
        course_id = course['key']
        course_name = course['title']
        workload = str(course['expected_duration']) + ' ' + course['expected_duration_unit']
        picture_url = course['image']
        course_description = course['summary']

        if len(course_description) >= 3000:
            course_description = course_description[:2800] + "..."

        Course.add_course(course_id,
                          course_name,
                          workload,
                          picture_url,
                          course_description)


# this function is return the plan template when user click on the plan url
@login_required
def plan_page(request):
    context = {}
    if not request.user:
        return Http404
    if request.method != 'GET':
        return Http404

    return render(request, 'plan.html', context)


# this function is return the plan template when user click on the plan url
@login_required
def plan_main(request):
    context = {}
    if not request.user:
        return Http404

    plans = Plan.get_activated_plan_by_user(request.user)
    if plans and len(plans) > 0:
        context['plans'] = plans
    sunday_plans = []
    monday_plans = []
    tuesday_plans = []
    wednesday_plans = []
    thursday_plans = []
    friday_plans = []
    saturday_plans = []

    for plan in plans:
        if plan.plan_day and plan.plan_day == 'Sunday':
            sunday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Monday':
            monday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Tuesday':
            tuesday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Wednesday':
            wednesday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Thursday':
            thursday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Friday':
            friday_plans.append(plan)
        elif plan.plan_day and plan.plan_day == 'Saturday':
            saturday_plans.append(plan)

    context['sunday_plans'] = sunday_plans
    context['monday_plans'] = monday_plans
    context['tuesday_plans'] = tuesday_plans
    context['wednesday_plans'] = wednesday_plans
    context['thursday_plans'] = thursday_plans
    context['friday_plans'] = friday_plans
    context['saturday_plans'] = saturday_plans

    return render(request, "plan_main.html", context)


# this function allows users to add their own plan
@login_required
def add_plan(request):
    context = {}
    if not request.user:
        return Http404
    if request.method != 'POST':
        return Http404

    if not 'day' in request.POST or not request.POST['day']:
        return Http404
    else:
        day = request.POST['day']

    if not 'from_hour' in request.POST or not request.POST['from_hour']:
        return Http404
    else:
        from_hour = request.POST['from_hour']

    if not 'from_minute' in request.POST or not request.POST['from_minute']:
        return Http404
    else:
        from_minute = request.POST['from_minute']

    if not 'from_ampm' in request.POST or not request.POST['from_ampm']:
        return Http404
    else:
        from_ampm = request.POST['from_ampm']

    if not 'to_hour' in request.POST or not request.POST['to_hour']:
        return Http404
    else:
        to_hour = request.POST['to_hour']

    if not 'to_minute' in request.POST or not request.POST['to_minute']:
        return Http404
    else:
        to_minute = request.POST['to_minute']

    if not 'to_ampm' in request.POST or not request.POST['to_ampm']:
        return Http404
    else:
        to_ampm = request.POST['to_ampm']

    if not 'course_name' in request.POST or not request.POST['course_name']:
        return Http404
    else:
        course_name = request.POST['course_name']

    Plan.add_plan_by_user(day,
                          from_hour,
                          from_minute,
                          from_ampm,
                          to_hour,
                          to_minute,
                          to_ampm,
                          course_name,
                          request.user)

    return render(request, 'plan.html', {})


# this function allows users to clear all their plans
@login_required
def clear_plan(request):
    current_plans = Plan.get_activated_plan_by_user(request.user)
    for plan in current_plans:
        Plan.deactivate_plan(plan.id)
    return HttpResponse(status=200)


# this fuction allows users to add their achievement
@login_required
def add_achievement(request, course_id):
    context = {}
    course = Course.get_course_by_key(course_id)
    context['course'] = course

    if request.method == 'GET':
        context['form'] = Achievement_form()
        return render(request, 'add_achievement.html', context)

    achievement_form = Achievement_form(request.POST)

    if not achievement_form.is_valid():
        context['form'] = {'form': achievement_form}
        return render(request, 'add_achievement.html', context)

    Achievement.add_achievement(request.user,
                                course,
                                achievement_form.cleaned_data['comment'],
                                achievement_form.cleaned_data['grade'],
                                achievement_form.cleaned_data['start_date'],
                                achievement_form.cleaned_data['end_date'],
                                achievement_form.cleaned_data['workload'])

    user = request.user
    new_comment = CourseComment(text=achievement_form.cleaned_data['comment'], user=user, Course=course)
    new_comment.save()

    return HttpResponseRedirect(reverse('course_profile', kwargs={'id': course_id}))


# this function returns all the users' achievements
@login_required
def achievement(request):
    context = {}
    achievement = Achievement.objects.filter(user=request.user)
    context['achievement'] = achievement
    return render(request, 'achievement.html', context)


# this function sort all the course by rating
@login_required
def sort_by_rating(request):
    context = {}
    course_list = Course.objects.all().distinct().order_by('-ratings__average', 'course_name')
    course = []
    for i in range(6):
        course.append(course_list[i])
    context['courses'] = course
    return render(request, 'main.html', context)


@login_required
def recommendation_on_users(request):
    current_user = request.user
    user_similarity_pairs = {}
    recommended_users = []
    courses = Course.objects.filter(user=current_user)
    # get the favorite collections of 1000 users recently logged in
    users = User.objects.all().order_by('-last_login').exclude(id=current_user.id).distinct()[:1000]
    for user in users:
        courses_other_user = Course.objects.filter(user=user)
        user_similarity_pairs[user] = calculate_cosine_similarity(request, courses, courses_other_user)

    sorted_users = sorted(user_similarity_pairs.items(), key=itemgetter(1), reverse=True)

    for sorted_user in sorted_users:
        recommended_users.append(sorted_user[0])

    return recommended_users[:6]


# this function get the recommended course for one user
@login_required
def recommend_by_similarity(request):
    current_user = request.user
    course_similarity_pairs = {}
    recommended_courses = []
    courses = Course.objects.filter(user=current_user)
    # get the favorite collections of 1000 users recently logged in
    users = User.objects.all().order_by('-last_login').exclude(id=current_user.id).distinct()[:1000]
    user_favorite_collections = get_user_favorite_collections(request, users)

    # for the course in the favorite collection of this user, get the recommended course
    for course in courses:
        recommended_courses_of_one_course = get_recommended_courses(request, course, user_favorite_collections)
        if recommended_courses_of_one_course:
            for k, v in recommended_courses_of_one_course.items():
                if k in course_similarity_pairs:
                    course_similarity_pairs[k] += v
                else:
                    course_similarity_pairs[k] = v

    sorted_courses = sorted(course_similarity_pairs.items(), key=itemgetter(1), reverse=True)

    for sorted_course in sorted_courses:
        recommended_courses.append(sorted_course[0])

    return recommended_courses


# this function get the recommended course for one specific course
@login_required
def get_recommended_courses(request, course, user_favorite_collections):
    recommend_courses = {}

    for user_favorite_collection in user_favorite_collections:
        if len(user_favorite_collection) != 0:
            similarity = calculate_cosine_similarity(request, [course], user_favorite_collection)
            for other_course in user_favorite_collection:
                if other_course in recommend_courses:
                    recommend_courses[other_course] += similarity
                else:
                    recommend_courses[other_course] = similarity

    if not course in recommend_courses:
        return
    recommend_courses.pop(course)
    return recommend_courses


@login_required
def calculate_cosine_similarity(request, course_list_1, course_list_2):
    if len(course_list_1) == 0 or len(course_list_2) == 0:
        return 0
    return float(count_match(request, course_list_1, course_list_2)) / math.sqrt(
        len(course_list_1) * len(course_list_2))


@login_required
def count_match(request, course_list_1, course_list_2):
    count = 0
    for course in course_list_1:
        if course in course_list_2:
            count += 1
    return count


# this function get all users' favorite course collections
@login_required
def get_user_favorite_collections(request, users):
    user_favorite_collections = []
    for user in users:
        user_favorite_collections.append(Course.objects.filter(user=user))
    return user_favorite_collections
