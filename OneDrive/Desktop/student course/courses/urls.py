from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/drop/', views.drop_course, name='drop_course'),
    path('admin/', views.admin_course_list, name='admin_course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_id>/announcement/create/', views.create_announcement, name='create_announcement'),
    path('<int:course_id>/attendance/', views.attendance_view, name='attendance'),
    path('<int:course_id>/my-attendance/', views.student_attendance, name='student_attendance'),
    path('<int:course_id>/videos/', views.course_videos, name='course_videos'),
    path('<int:course_id>/videos/add/', views.add_course_video, name='add_course_video'),
    path('<int:course_id>/videos/<int:video_id>/edit/', views.edit_course_video, name='edit_course_video'),
    path('<int:course_id>/videos/<int:video_id>/delete/', views.delete_course_video, name='delete_course_video'),
    path('<int:course_id>/videos/search/', views.search_youtube_videos_view, name='search_youtube_videos'),
    path('<int:course_id>/videos/<int:video_id>/view/', views.view_course_video, name='view_course_video'),
] 