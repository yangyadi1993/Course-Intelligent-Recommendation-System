from django.conf.urls import url

from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete
import finalproject.views

urlpatterns = [

    url(r'^$', finalproject.views.home, name='home'),

    url(r'^home_linkedin$', finalproject.views.home_linkedin, name='home_linkedin'),

    url(r'^login$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout_then_login, name='logout'),

    url(r'^search$', finalproject.views.search, name='search'),

    url(r'^linkedin_logout$', finalproject.views.linkedin_logout, name='linkedin_logout'),
    url(r'^course/(?P<id>.*)$', finalproject.views.get_course, name='course_profile'),
    url(r'^course_addcoursecomment/(?P<key>.*)$', finalproject.views.get_course_2, name='course_2'),
    url(r'^achievement/(?P<course_id>.*)$', finalproject.views.add_achievement, name='add_achievement'),
    url(r'^achievement', finalproject.views.achievement, name='achievement'),
    url(r'^sort', finalproject.views.sort_by_rating, name='sort_by_rating'),
    url(r'^get_photo/(?P<id>\d+)', finalproject.views.get_photo, name='get_photo'),
    url(r'^get_profile', finalproject.views.get_profile, name='get_profile'),

    url(r'^register', finalproject.views.register, name='register'),
    url(
        r'^confirm/(?P<email>[a-z_0-9.-]{1,64}@([a-z0-9-]{1,200}.){1,5}[a-z]{1,6})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        finalproject.views.confirm_registration, name='confirm_registration'),
    url(r'^user/password/reset/$', finalproject.views.password_reset, name='password_reset'),
    url(r'^user/password/reset/done/$', password_reset_done,
        {'template_name': 'password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, {'template_name': 'password_reset_confirm.html',
                                 'post_reset_redirect': '/finalproject/user/password/done/'}, name='password_reset_email'),
    url(r'^user/password/done/$', password_reset_complete,
        {'template_name': 'password_reset_complete.html'}),

    url(r'^other_user_profile/(?P<id>\d+)', finalproject.views.other_user_profile, name='other_user_profile'),

    url(r'^profile_info', finalproject.views.profile_info, name='profile_info'),
    url(r'^update_info', finalproject.views.update_info, name='update_info'),
    url(r'^upload_avatar', finalproject.views.upload_avatar, name='upload_avatar'),

    url(r'^education_load$', finalproject.views.education_load, name='education_load'),
    url(r'^add_education$', finalproject.views.add_education, name='add_education'),

    url(r'^skill_load$', finalproject.views.skill_load, name='skill_load'),
    url(r'^add_skill$', finalproject.views.add_skill, name='add_skill'),

    url(r'^work_experience_load$', finalproject.views.work_experience_load, name='work_experience_load'),
    url(r'^add_work_experience$', finalproject.views.add_work_experience, name='add_work_experience'),

    url(r'^honor_load$', finalproject.views.honor_load, name='honor_load'),
    url(r'^add_honor$', finalproject.views.add_honor, name='add_honor'),

    url(r'^project_load$', finalproject.views.project_load, name='project_load'),
    url(r'^add_project$', finalproject.views.add_project, name='add_project'),

    url(r'^language_load$', finalproject.views.language_load, name='language_load'),
    url(r'^add_language$', finalproject.views.add_language, name='add_language'),

    url(r'^collection$', finalproject.views.get_collection, name='collection'),
    url(r'^addcollection/(?P<id>.*)$', finalproject.views.add_collection, name='add_collection'),
    url(r'^removecollection/(?P<id>.*)$', finalproject.views.remove_collection, name='remove_collection'),
    url(r'^addcoursecomment/(?P<id>.*)$', finalproject.views.create_coursecomment, name='create_coursecomment'),

    url(r'^plan_page', finalproject.views.plan_page, name='plan_page'),
    url(r'^plan_main', finalproject.views.plan_main, name='plan_main'),
    url(r'^add_plan', finalproject.views.add_plan, name='add_plan'),
    url(r'^clear_plan', finalproject.views.clear_plan, name='clear_plan'),

    url(r'^page_upload_resume', finalproject.views.page_upload_resume, name='page_upload_resume'),

]
