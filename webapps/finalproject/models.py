from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


def user_directory_path(instance, filename):
    return instance.__class__.__name__ + '/' + str(uuid.uuid4()) + filename


def resume_directory_path(instance, filename):
    return instance.__class__.__name__ + '/' + str(uuid.uuid4()) + filename


# Create your models here.

class Search_history(models.Model):
    user = models.ForeignKey(User)
    history1 = models.CharField(max_length=255, null=True, blank=True)
    history2 = models.CharField(max_length=255, null=True, blank=True)


class User_profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15, null=True, default="", blank=True)
    summary = models.CharField(max_length=420, null=True, default="Say something about your self.", blank=True)
    picture = models.ImageField(upload_to=user_directory_path,
                                default="user1.png")
    location = models.CharField(max_length=500, null=True, default="", blank=True)
    industry = models.CharField(max_length=500, null=True, default="", blank=True)
    picture_url = models.URLField(max_length=500, null=True, blank=True)

    # collection = models.ForeignKey(Collection, null=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_user_profile_by_user(user):
        return User_profile.objects.get(user=user)

    @staticmethod
    def get_user_profile_by_id(id):
        return User_profile.objects.get(id=id)

    @staticmethod
    def create_user_profile(user, phone, location, industry):
        new_user_profile = User_profile(user=user,
                                        phone=phone,
                                        location=location,
                                        industry=industry)
        new_user_profile.save()
        return new_user_profile

    @staticmethod
    def update_user_profile(user, phone, summary, location, industry):
        user_profile = User_profile.get_user_profile_by_user(user)
        user_profile.phone = phone
        user_profile.summary = summary
        user_profile.location = location
        user_profile.industry = industry
        user_profile.save()
        return user_profile


class ModelFile(models.Model):
    user = models.OneToOneField(User)
    file = models.FileField(upload_to=resume_directory_path, null=True, blank=True)


class Course(models.Model):
    course_id = models.CharField(max_length=255, null=True)
    course_name = models.CharField(max_length=255, null=True)
    course_load = models.CharField(max_length=255, null=True)
    picture_url = models.CharField(max_length=255, null=True)
    course_description = models.CharField(max_length=3000, null=True)
    user = models.ManyToManyField(User)
    ratings = GenericRelation(Rating, related_query_name='ratings')

    def __unicode__(self):
        return self.course_id

    @staticmethod
    def add_course(course_id, course_name, course_load, picture_url, course_description):
        new_course = Course(course_id=course_id,
                            course_name=course_name,
                            course_load=course_load,
                            picture_url=picture_url,
                            course_description=course_description)
        new_course.save()
        return new_course

    @staticmethod
    def get_courses_by_user(user):
        return Course.objects.filter(user=user)

    @staticmethod
    def get_course_by_key(course_id):
        return Course.objects.get(course_id=course_id)

    @staticmethod
    def get_course_by_name(course_name):
        return Course.objects.get(course_name=course_name)

    @staticmethod
    def search_course_by_name(search):
        return Course.objects.filter(course_name__icontains=search)

    @staticmethod
    def search_course_by_description(search):
        return Course.objects.filter(course_description__icontains=search)


class CourseComment(models.Model):
    text = models.TextField(max_length=42)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    street_one = models.CharField(max_length=255, null=False, default="", blank=True)
    street_two = models.CharField(max_length=255, null=False, default="", blank=True)
    city = models.CharField(max_length=255, null=False, default="", blank=True)
    state_province = models.CharField(max_length=255, null=False, default="", blank=True)
    country = models.CharField(max_length=255, null=False, default="", blank=True)
    post_code = models.IntegerField(null=True, default=0, blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_address_by_user(user):
        return Address.objects.filter(user=user)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    school_name = models.CharField(max_length=255, null=False, default="", blank=True)
    degree = models.CharField(max_length=255, null=False, default="", blank=True)
    major = models.CharField(max_length=255, null=False, default="", blank=True)
    minor = models.CharField(max_length=255, null=False, default="", blank=True)
    start_date = models.DateField(null=True, blank=True)
    graduate_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_education_by_user(user):
        return Education.objects.filter(user=user)

    @staticmethod
    def add_education_by_user(user, school_name, degree, major, minor, start_date, graduate_date):
        new_education = Education(user=user,
                                  school_name=school_name,
                                  degree=degree,
                                  major=major,
                                  minor=minor,
                                  start_date=start_date,
                                  graduate_date=graduate_date)
        new_education.save()
        return new_education


class Academic_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    project_name = models.CharField(max_length=255, null=False, default="", blank=True)
    organization_name = models.CharField(max_length=255, null=False, default="", blank=True)
    responsibility = models.CharField(max_length=255, null=False, default="", blank=True)
    description = models.CharField(max_length=255, null=False, default="", blank=True)
    start_date = models.DateField(null=True, default="", blank=True)
    end_date = models.DateField(null=True, default="", blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_academic_project_by_user(user):
        return Academic_project.objects.filter(user=user)

    @staticmethod
    def add_academic_project_by_user(user, project_name, organization_name, responsibility, description,
                                     start_date, end_date):
        new_adademic_project = Academic_project(user=user,
                                                project_name=project_name,
                                                organization_name=organization_name,
                                                responsibility=responsibility,
                                                description=description,
                                                start_date=start_date,
                                                end_date=end_date)
        new_adademic_project.save()
        return new_adademic_project


class Work_experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    employer_name = models.CharField(max_length=255, null=False, default="", blank=True)
    location_city = models.CharField(max_length=255, null=False, default="", blank=True)
    location_country = models.CharField(max_length=255, null=False, default="", blank=True)
    responsibility = models.CharField(max_length=255, null=False, default="", blank=True)
    description = models.CharField(max_length=255, null=False, default="", blank=True)
    start_date = models.DateField(null=True, default="", blank=True)
    end_date = models.DateField(null=True, default="", blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_work_experience_by_user(user):
        return Work_experience.objects.filter(user=user)

    @staticmethod
    def add_work_experience_by_user(user, employer_name, location_city, location_country, responsibility,
                                    description, start_date, end_date):
        new_work_experience = Work_experience(user=user,
                                              employer_name=employer_name,
                                              location_city=location_city,
                                              location_country=location_country,
                                              responsibility=responsibility,
                                              description=description,
                                              start_date=start_date,
                                              end_date=end_date)
        new_work_experience.save()
        return new_work_experience


class Honor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    title = models.CharField(max_length=255, null=False, default="", blank=True)
    issued_organization = models.CharField(max_length=255, null=False, default="", blank=True)
    issued_date = models.DateField(null=True, default="", blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_honor_by_user(user):
        return Honor.objects.filter(user=user)

    @staticmethod
    def add_honor_by_user(user, title, issued_organization, issued_date):
        new_honor = Honor(user=user,
                          title=title,
                          issued_organization=issued_organization,
                          issued_date=issued_date)
        new_honor.save()
        return new_honor


class Skill_set(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    skill_name = models.CharField(max_length=255, null=False, default="", blank=True)
    proficiency = models.CharField(max_length=255, null=False, default="", blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_skill_set_by_user(user):
        return Skill_set.objects.filter(user=user)

    @staticmethod
    def add_skill_by_user(user, skill_name, proficiency):
        new_skill = Skill_set(user=user,
                              skill_name=skill_name,
                              proficiency=proficiency)
        new_skill.save()
        return new_skill


class Language_set(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    language_name = models.CharField(max_length=255, null=False, default="", blank=True)
    proficiency = models.CharField(max_length=255, null=False, default="", blank=True)

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_language_set_by_user(user):
        return Language_set.objects.filter(user=user)

    @staticmethod
    def add_language_by_user(user, language_name, proficiency):
        new_language = Language_set(user=user,
                                    language_name=language_name,
                                    proficiency=proficiency)
        new_language.save()
        return new_language


class Plan(models.Model):
    plan_day = models.CharField(max_length=255, null=False, default="")
    plan_from_hour = models.CharField(max_length=255, null=False, default="00")
    plan_from_minute = models.CharField(max_length=2, null=False, default="00")
    plan_from_ampm = models.CharField(max_length=255, null=False, default="am")
    plan_to_hour = models.CharField(max_length=2, null=False, default="00")
    plan_to_minute = models.CharField(max_length=2, null=False, default="00")
    plan_to_ampm = models.CharField(max_length=255, null=False, default="am")
    plan_course_name = models.CharField(max_length=255, null=True)
    plan_activated = models.BooleanField(null=False, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")

    def __unicode__(self):
        return self.user

    @staticmethod
    def get_activated_plan_by_user(user):
        return Plan.objects.filter(user=user, plan_activated=True).distinct()

    @staticmethod
    def get_all_plan_by_user(user):
        return Plan.objects.filter(user=user)

    @staticmethod
    def deactivate_plan(id):
        plan_to_deactivate = Plan.objects.get(id=id)
        if not plan_to_deactivate:
            return
        plan_to_deactivate.plan_activated = False
        plan_to_deactivate.save()
        return plan_to_deactivate

    @staticmethod
    def add_plan_by_user(plan_day, plan_from_hour, plan_from_minute, plan_from_ampm,
                         plan_to_hour, plan_to_minute, plan_to_ampm, plan_course_name, user):
        new_plan = Plan(plan_day=plan_day,
                        plan_from_hour=plan_from_hour,
                        plan_from_minute=plan_from_minute,
                        plan_from_ampm=plan_from_ampm,
                        plan_to_hour=plan_to_hour,
                        plan_to_minute=plan_to_minute,
                        plan_to_ampm=plan_to_ampm,
                        plan_course_name=plan_course_name,
                        plan_activated=True,
                        user=user)

        new_plan.save()
        return new_plan


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, default="")
    comment = models.CharField(max_length=500, null=False, default="", blank=True)
    grade = models.CharField(max_length=255, null=False, default="", blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    workload = models.IntegerField(null=True, default=0, blank=True)

    @staticmethod
    def add_achievement(user, course, comment, grade, start_date, end_date, workload):
        new_achievement = Achievement(user=user,
                                      course=course,
                                      comment=comment,
                                      grade=grade,
                                      start_date=start_date,
                                      end_date=end_date,
                                      workload=workload)
        new_achievement.save()
        return new_achievement
