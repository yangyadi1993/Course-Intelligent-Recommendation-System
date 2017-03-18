from django.test import TestCase, Client, RequestFactory
from finalproject.models import *
import finalproject.views
from django.contrib.auth.models import User


# Create your tests here.
class Add_plan_test(TestCase):
    def get_plan(self):
        client = Client()
        response = client.get('/finalproject/plan_main')
        self.assertTrue(response.status_code == 200)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def get_plan_test(self):
        request = self.factory.get('/finalproject/plan_main')
        request.user = self.user
        response = finalproject.views.plan_main(request)
        self.assertTrue(response.status_code == 200)

    def test_add_plan(self):
        client = Client()

        sample_plan_day = 'Monday'
        sample_plan_from_hour = '09'
        sample_plan_from_minute = '00'
        sample_plan_from_ampm = 'am'
        sample_plan_to_hour = '10'
        sample_plan_to_minute = '30'
        sample_plan_to_ampm = 'am'
        sample_plan_course_name = 'Computer Science'

        response = client.post('/finalproject/add_plan', {
            'day': sample_plan_day,
            'from_hour': sample_plan_from_hour,
            'from_minute': sample_plan_from_minute,
            'from_ampm': sample_plan_from_ampm,
            'to_hour': sample_plan_to_hour,
            'to_minute': sample_plan_to_minute,
            'to_ampm': sample_plan_to_ampm,
            'course_name': sample_plan_course_name
        })
        self.assertTrue(response.status_code != 404)


class Add_Collection_test(TestCase):
    def test_add_collection(self):
        client = Client()
        id = 'wWkoAThyEea67A6Z1aCfuw'
        response = client.post('/finalproject/addcollection/' + id)
        self.assertTrue(response.status_code == 302)


class Login_test(TestCase):
    def login_get(self):
        client = Client()
        response = client.get('/finalproject/login')
        self.assertTrue(response.status_code == 200)

    def test_login(self):
        client = Client()
        username = 'tester'
        password = '111111'
        response = client.post('/finalproject/login', {
            'username': username,
            'password': password
        })
        self.assertTrue(response.status_code != 404)


class Get_profile_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester',
            email='sjing@cmu.edu.com',
            password='111111',
        )

    def get_plan(self):
        request = self.factory.get('/finalproject/get_profile')
        request.user = self.user
        response = finalproject.views.profile_info(request)
        self.assertTrue(response.status_code == 200)


class Get_home_test(TestCase):
    def test_home(self):
        client = Client()
        response = client.get('/finalproject')
        self.assertTrue(response.status_code != 404)


class Get_course_test(TestCase):
    def test_get_course(self):
        client = Client()
        id = 'wWkoAThyEea67A6Z1aCfuw'
        response = client.post('/finalproject/course/' + id)
        self.assertTrue(response.status_code != 404)


class Remove_collection_test(TestCase):
    def test_remove_collection_post(self):
        client = Client()
        id = 'wWkoAThyEea67A6Z1aCfuw'
        response = client.post('/finalproject/removecollection/' + id)
        self.assertTrue(response.status_code != 404)


class Get_collection_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def get_collection_test(self):
        request = self.factory.get('/finalproject/collection')
        request.user = self.user
        response = finalproject.views.get_collection(request)
        self.assertTrue(response.status_code == 200)


class Get_course_comment_test(TestCase):
    def test_get_course(self):
        client = Client()
        id = 'wWkoAThyEea67A6Z1aCfuw'
        response = client.post('/finalproject/addcoursecomment/' + id)
        self.assertTrue(response.status_code != 404)


class Register_test(TestCase):
    def test_register(self):
        client = Client()
        username = 'tester'
        password = '111111'
        email = 'sjing@andrew.cmu.edu'
        first_name = 'Shiqing'
        last_name = 'Jing'

        response = client.post('/finalproject/register', {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        self.assertTrue(response.status_code != 404)


class Get_photo_test(TestCase):
    def test_get_photo(self):
        client = Client()
        id = '1'
        response = client.post('/finalproject/get_photo/' + id)
        self.assertTrue(response.status_code != 404)


class Search_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_search(self):
        search = 'math'
        request = self.factory.get('/finalproject/search', {'search': search})
        request.user = self.user

        response = finalproject.views.search(request)

        self.assertTrue(response.status_code != 404)


class Add_education_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_education')
        request.user = self.user
        response = finalproject.views.add_education(request)
        self.assertTrue(response.status_code == 302)

    def test_add_education(self):
        client = Client()
        school_name = 'CMU'
        degree = 'master'
        major = 'Computer Science'
        minor = 'mism'
        country = 'US'
        start_date = '2015-08-20'
        graduate_date = '2017-05-19'
        user = 'sjing'
        response = client.post('/finalproject/add_education', {
            'user': user,
            'school_name': school_name,
            'degree': degree,
            'major': major,
            'minor': minor,
            'country': country,
            'start_date': start_date,
            'graduate_date': graduate_date
        })
        self.assertTrue(response.status_code == 302)


class Add_skill_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_skill')
        request.user = self.user
        response = finalproject.views.add_skill(request)
        self.assertTrue(response.status_code == 302)

    def test_add_skill(self):
        client = Client()
        skill_name = 'java'
        proficiency = 'good'

        response = client.post('/finalproject/add_skill', {
            'skill_name': skill_name,
            'proficiency': proficiency
        })
        self.assertTrue(response.status_code == 302)


class Add_work_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_work')
        request.user = self.user
        response = finalproject.views.add_work_experience(request)
        self.assertTrue(response.status_code == 302)

    def test_add_work(self):
        client = Client()
        employer_name = 'Google'
        location_city = 'San Fransisco'
        location_country = 'US'
        responsibility = 'Web Developer'
        description = 'Develop website with python'
        start_date = '2015-08-20'
        end_date = '2017-05-19'

        response = client.post('/finalproject/add_work_experience', {
            'employer_name': employer_name,
            'location_city': location_city,
            'location_country': location_country,
            'responsibility': responsibility,
            'description': description,
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertTrue(response.status_code == 302)


class Add_honor_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_honor')
        request.user = self.user
        response = finalproject.views.add_honor(request)
        self.assertTrue(response.status_code == 302)

    def test_add_honor(self):
        client = Client()
        title = 'first class'
        issued_organization = 'CMU'
        issued_date = '2015-08-20'
        user = 'sjing'
        response = client.post('/finalproject/add_honor', {
            'user': user,
            'title': title,
            'issued_organization': issued_organization,
            'issued_date': issued_date
        })
        self.assertTrue(response.status_code == 302)


class Add_project_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_project')
        request.user = self.user
        response = finalproject.views.add_project(request)
        self.assertTrue(response.status_code == 302)

    def test_add_project(self):
        client = Client()
        project_name = 'mentor'
        organization_name = 'master'
        responsibility = 'Back End'
        description = 'Recommend course for user'
        start_date = '2016-08-20'
        end_date = '2017-05-19'
        user = 'sjing'
        response = client.post('/finalproject/add_project', {
            'user': user,
            'project_name': project_name,
            'organization_name': organization_name,
            'responsibility': responsibility,
            'description': description,
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertTrue(response.status_code == 302)


class Add_language_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='password',
        )

    def test_get_profile(self):
        request = self.factory.get('/finalproject/add_language')
        request.user = self.user
        response = finalproject.views.add_language(request)
        self.assertTrue(response.status_code == 302)

    def test_add_skill(self):
        client = Client()
        language_name = 'English'
        proficiency = 'good'

        response = client.post('/finalproject/add_language', {
            'language_name': language_name,
            'proficiency': proficiency
        })
        self.assertTrue(response.status_code == 302)
