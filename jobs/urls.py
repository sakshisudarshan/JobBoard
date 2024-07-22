from django.urls import path
from .views import  application_success, download_resume, employer_dashboard, employer_search, employer_signup, home, job_posted_success, job_search, job_search_results, job_seeker_dashboard, job_seeker_signup, login_page, employer_login, job_seeker_login, post_job, signup

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signup/job_seeker/', job_seeker_signup, name='job_seeker_signup'),
    path('signup/employer/', employer_signup, name='employer_signup'),
    path('login/', login_page, name='login'),
    path('login/job_seeker/', job_seeker_login, name='job_seeker_login'),
    path('login/employer/', employer_login, name='employer_login'),
    path('dashboard/job_seeker/', job_seeker_dashboard, name='job_seeker_dashboard'),
    path('job_search/', job_search, name='job_search'),
    path('job_search_results/',job_search_results, name='job_search_results'),
    path('application_success/', application_success, name='application_success'),
    path('employer_dashboard/', employer_dashboard, name='employer_dashboard'),
    path('employer_search/', employer_search, name='employer_search'),
    path('download_resume/<int:application_id>/', download_resume, name='download_resume'),
    path('post_job/', post_job, name='post_job'),
    path('job_posted_success/', job_posted_success, name='job_posted_success'),
]
