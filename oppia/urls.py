# oppia/urls.py
from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views import static
from django.views.generic import TemplateView
from oppia import views as oppia_views


# Custom HTTP response pages
handler403 = 'oppia.permissions.oppia_403_handler'

app_name = 'oppia'
urlpatterns = [

    path(r'', oppia_views.home_view, name="index"),
    path(r'server/', oppia_views.server_view, name="server"),
    path(r'about/', oppia_views.about_view, name="about"),

    path(r'teacher', oppia_views.teacher_home_view,
        name="teacher_index"),

    path(r'leaderboard', oppia_views.leaderboard_view,
        name="leaderboard"),
    path(r'upload',
        oppia_views.upload_step1,
        name="upload"),
    path(r'upload2/<int:course_id>',
        oppia_views.upload_step2,
        name="upload_step2"),
    path(r'upload2/success',
        TemplateView.as_view(template_name="course/upload-success.html"),
        name="upload_success"),
    path(r'course/',
        oppia_views.courses_list_view,
        name="course"),
    path(r'course/tag/<int:tag_id>',
        oppia_views.tag_courses_view,
        name="tag_courses"),
    path(r'course/<int:course_id>/',
        oppia_views.recent_activity,
        name="recent_activity"),
    path(r'course/<int:course_id>/edit/',
        oppia_views.upload_step2,
        {'editing': True},
        name="course_edit"),
    path(r'course/<int:course_id>/detail/',
        oppia_views.recent_activity_detail,
        name="recent_activity_detail"),
    path(r'course/<int:course_id>/detail/export/',
        oppia_views.export_tracker_detail,
        name="export_tracker_detail"),
    path(r'course/<int:course_id>/download',
        oppia_views.CourseDownload.as_view(),
        name="course_download"),

    path(r'cohort/',
        oppia_views.cohort_list_view,
        name="cohorts"),
    path(r'cohort/add/',
        oppia_views.cohort_add,
        name="cohort_add"),
    path(r'cohort/(<int:cohort_id>/edit/',
        oppia_views.cohort_edit,
        name="cohort_edit"),
    path(r'cohort/<int:cohort_id>)/view/',
        oppia_views.cohort_view,
        name="cohort_view"),
    path(r'cohort/(<int:cohort_id>/(<int:course_id>/view/',
        oppia_views.cohort_course_view,
        name="cohort_course_view"),
    path(r'cohort/(<int:cohort_id>/leaderboard',
        oppia_views.cohort_leaderboard_view,
        name="cohort_leaderboard"),

    path(r'view/',
        oppia_views.app_launch_activity_redirect_view,
        name="app_launch_activity_redirect"),
    url(r'^media/(?P<path>.*)$',
        static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
