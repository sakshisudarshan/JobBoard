from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import JobApplication
from django.urls import reverse
from .forms import JobPostingForm
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'jobs/homepage.html')


def signup(request):
    return render(request, 'jobs/signup.html')


def job_seeker_signup(request):
    if request.method == 'POST':
        full_name = request.POST['fullName']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()
        return redirect('job_seeker_login') 
    return render(request, 'jobs/job_seeker_signup.html')


def employer_signup(request):
    if request.method == 'POST':
        company_name = request.POST['companyName']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = company_name
        user.save()
        return redirect('employer_login')  
    return render(request, 'jobs/employer_signup.html')


def login_page(request):
    return render(request, 'jobs/login.html')


def job_seeker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('job_seeker_dashboard')  
        else:
            return render(request, 'jobs/job_seeker_login.html', {'error': 'Invalid credentials'})
    return render(request, 'jobs/job_seeker_login.html')


def employer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('employer_dashboard')  
            else:
                return render(request, 'jobs/employer_login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'jobs/employer_login.html', {'error': 'Please provide both email and password'})

    return render(request, 'jobs/employer_login.html')


@login_required
def job_seeker_dashboard(request):
    return render(request, 'jobs/job_seeker_dashboard.html')


@login_required
def employer_dashboard(request):
    return render(request, 'jobs/employer_dashboard.html')


def job_search(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        resume = request.FILES.get('resume')
        
        if job_title and job_description and resume:
            JobApplication.objects.create(
                job_title=job_title,
                job_description=job_description,
                applicant_resume=resume
            )
            return redirect(reverse('application_success'))

    job_type = request.GET.get('job_type')
    domain = request.GET.get('domain')
    location = request.GET.get('location')

    job_data = {
           
        ('full-time', 'graphic-design', 'Bangalore'): [
            {'title': 'Senior Graphic Designer', 'description': 'Work on high-profile projects in Bangalore.'},
            {'title': 'Junior Graphic Designer', 'description': 'Assist in designing marketing materials.'}
        ],

        ('full-time', 'graphic-design', 'Mumbai'): [
            {'title': 'Senior Graphic Designer', 'description': 'Work on high-profile projects in Mumbai.'},
            {'title': 'Junior Graphic Designer', 'description': 'Assist in designing marketing materials.'}
        ],
         ('full-time', 'graphic-design', 'Pune'): [
            {'title': 'Senior Graphic Designer', 'description': 'Work on high-profile projects in Pune.'},
            {'title': 'Junior Graphic Designer', 'description': 'Assist in designing marketing materials.'}
        ],
         ('full-time', 'graphic-design', 'Delhi'): [
            {'title': 'Senior Graphic Designer', 'description': 'Work on high-profile projects in Delhi.'},
            {'title': 'Junior Graphic Designer', 'description': 'Assist in designing marketing materials.'}
        ],
        ('full-time', 'web-development', 'Bangalore'): [
        {'title': 'Senior Web Developer', 'description': 'Lead the development team on exciting web projects in Bangalore.'},
        {'title': 'Front-End Developer', 'description': 'Create engaging user interfaces and optimize user experience.'},
        {'title': 'Back-End Developer', 'description': 'Build robust server-side applications and APIs for scalable web solutions.'}
        ],
        ('full-time', 'web-development', 'Mumbai'): [
        {'title': 'Senior Web Developer', 'description': 'Lead the development team on exciting web projects in Bangalore.'},
        {'title': 'Front-End Developer', 'description': 'Create engaging user interfaces and optimize user experience.'},
        {'title': 'Back-End Developer', 'description': 'Build robust server-side applications and APIs for scalable web solutions.'}
        ],
        ('full-time', 'web-development', 'Delhi'): [
        {'title': 'Senior Web Developer', 'description': 'Lead the development team on exciting web projects in Bangalore.'},
        {'title': 'Front-End Developer', 'description': 'Create engaging user interfaces and optimize user experience.'},
        {'title': 'Back-End Developer', 'description': 'Build robust server-side applications and APIs for scalable web solutions.'}
        ],
        ('full-time', 'web-development', 'Pune'): [
        {'title': 'Senior Web Developer', 'description': 'Lead the development team on exciting web projects in Bangalore.'},
        {'title': 'Front-End Developer', 'description': 'Create engaging user interfaces and optimize user experience.'},
        {'title': 'Back-End Developer', 'description': 'Build robust server-side applications and APIs for scalable web solutions.'}
        ],
        ('full-time', 'data-science', 'Bangalore'): [
        {'title': 'Senior Data Scientist', 'description': 'Lead data science projects in Bangalore.'},
        {'title': 'Data Scientist', 'description': 'Work on data analysis and machine learning tasks.'}
        ],
         ('full-time', 'data-science', 'Pune'): [
        {'title': 'Senior Data Scientist', 'description': 'Lead data science projects in Bangalore.'},
        {'title': 'Data Scientist', 'description': 'Work on data analysis and machine learning tasks.'}
        ],
         ('full-time', 'data-science', 'Delhi'): [
        {'title': 'Senior Data Scientist', 'description': 'Lead data science projects in Bangalore.'},
        {'title': 'Data Scientist', 'description': 'Work on data analysis and machine learning tasks.'}
        ],
         ('full-time', 'data-science', 'Mumbai'): [
        {'title': 'Senior Data Scientist', 'description': 'Lead data science projects in Bangalore.'},
        {'title': 'Data Scientist', 'description': 'Work on data analysis and machine learning tasks.'}
        ],
        ('full-time', 'marketing', 'Bangalore'): [
        {'title': 'Marketing Manager', 'description': 'Lead marketing initiatives in Bangalore.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Execute digital campaigns for local markets.'}
        ],
         ('full-time', 'marketing', 'Pune'): [
        {'title': 'Marketing Manager', 'description': 'Lead marketing initiatives in Bangalore.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Execute digital campaigns for local markets.'}
        ],
         ('full-time', 'marketing', 'Mumbai'): [
        {'title': 'Marketing Manager', 'description': 'Lead marketing initiatives in Bangalore.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Execute digital campaigns for local markets.'}
        ],
         ('full-time', 'marketing', 'Delhi'): [
        {'title': 'Marketing Manager', 'description': 'Lead marketing initiatives in Bangalore.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Execute digital campaigns for local markets.'}
        ],
         ('part-time', 'graphic-design', 'Bangalore'): [
        {'title': 'Part-Time Graphic Designer', 'description': 'Create visually appealing graphics for marketing materials on a flexible schedule.'},
        {'title': 'Freelance Graphic Designer', 'description': 'Work remotely on graphic design projects, collaborating with clients as needed.'}
         ],
         ('part-time', 'graphic-design', 'Pune'): [
        {'title': 'Part-Time Graphic Designer', 'description': 'Create visually appealing graphics for marketing materials on a flexible schedule.'},
        {'title': 'Freelance Graphic Designer', 'description': 'Work remotely on graphic design projects, collaborating with clients as needed.'}
         ],
         ('part-time', 'graphic-design', 'Delhi'): [
        {'title': 'Part-Time Graphic Designer', 'description': 'Create visually appealing graphics for marketing materials on a flexible schedule.'},
        {'title': 'Freelance Graphic Designer', 'description': 'Work remotely on graphic design projects, collaborating with clients as needed.'}
         ],
         ('part-time', 'graphic-design', 'Mumbai'): [
        {'title': 'Part-Time Graphic Designer', 'description': 'Create visually appealing graphics for marketing materials on a flexible schedule.'},
        {'title': 'Freelance Graphic Designer', 'description': 'Work remotely on graphic design projects, collaborating with clients as needed.'}
         ],
        ('part-time', 'web-development', 'Bangalore'): [
            {'title': 'Part-Time Web Developer', 'description': 'Develop websites for local businesses.'},
            {'title': 'Front-End Developer', 'description': 'Focus on front-end development tasks.'}
        ],
         ('part-time', 'web-development', 'Pune'): [
            {'title': 'Part-Time Web Developer', 'description': 'Develop websites for local businesses.'},
            {'title': 'Front-End Developer', 'description': 'Focus on front-end development tasks.'}
        ],
         ('part-time', 'web-development', 'Mumbai'): [
            {'title': 'Part-Time Web Developer', 'description': 'Develop websites for local businesses.'},
            {'title': 'Front-End Developer', 'description': 'Focus on front-end development tasks.'}
        ],
         ('part-time', 'web-development', 'Delhi'): [
            {'title': 'Part-Time Web Developer', 'description': 'Develop websites for local businesses.'},
            {'title': 'Front-End Developer', 'description': 'Focus on front-end development tasks.'}
        ],
        ('part-time', 'data-science', 'Bangalore'): [
        {'title': 'Part-Time Data Scientist', 'description': 'Analyze data and create insights for local startups.'},
        {'title': 'Junior Data Analyst', 'description': 'Assist in data analysis tasks.'}
        ],
         ('part-time', 'data-science', 'Pune'): [
        {'title': 'Part-Time Data Scientist', 'description': 'Analyze data and create insights for local startups.'},
        {'title': 'Junior Data Analyst', 'description': 'Assist in data analysis tasks.'}
        ],
         ('part-time', 'data-science', 'Mumbai'): [
        {'title': 'Part-Time Data Scientist', 'description': 'Analyze data and create insights for local startups.'},
        {'title': 'Junior Data Analyst', 'description': 'Assist in data analysis tasks.'}
        ],
         ('part-time', 'data-science', 'Delhi'): [
        {'title': 'Part-Time Data Scientist', 'description': 'Analyze data and create insights for local startups.'},
        {'title': 'Junior Data Analyst', 'description': 'Assist in data analysis tasks.'}
        ],
            ('part-time', 'marketing', 'Bangalore'): [
        {'title': 'Part-Time Marketing Associate', 'description': 'Support marketing initiatives in Bangalore.'},
        {'title': 'Marketing Assistant', 'description': 'Assist in executing marketing strategies.'}
        ],
        ('part-time', 'marketing', 'Mumbai'): [
        {'title': 'Part-Time Marketing Associate', 'description': 'Support marketing initiatives in Mumbai.'},
        {'title': 'Marketing Assistant', 'description': 'Assist in executing marketing strategies.'}
        ],
        ('part-time', 'marketing', 'Delhi'): [
        {'title': 'Part-Time Marketing Associate', 'description': 'Support marketing initiatives in Delhi.'},
        {'title': 'Marketing Assistant', 'description': 'Assist in executing marketing strategies.'}
        ],
        ('part-time', 'marketing', 'Pune'): [
        {'title': 'Part-Time Marketing Associate', 'description': 'Support marketing initiatives in Pune.'},
        {'title': 'Marketing Assistant', 'description': 'Assist in executing marketing strategies.'}
         ],
         ('freelance', 'data-science', 'Bangalore'): [
        {'title': 'Freelance Data Scientist', 'description': 'Analyze large datasets for clients in Bangalore.'},
        {'title': 'Machine Learning Specialist', 'description': 'Implement machine learning models in Bangalore.'}
        ],
        ('freelance', 'data-science', 'Mumbai'): [
        {'title': 'Freelance Data Scientist', 'description': 'Analyze large datasets for clients in Mumbai.'},
        {'title': 'Machine Learning Specialist', 'description': 'Implement machine learning models in Mumbai.'}
        ],
        ('freelance', 'data-science', 'Pune'): [
        {'title': 'Freelance Data Scientist', 'description': 'Analyze large datasets for clients in Pune.'},
        {'title': 'Machine Learning Specialist', 'description': 'Implement machine learning models in Pune.'}
        ],
        ('freelance', 'data-science', 'Delhi'): [
        {'title': 'Freelance Data Scientist', 'description': 'Analyze large datasets for clients in Delhi.'},
        {'title': 'Machine Learning Specialist', 'description': 'Implement machine learning models in Delhi.'}
        ],
        ('freelance', 'marketing', 'Bangalore'): [
        {'title': 'Freelance Marketing Consultant', 'description': 'Develop marketing strategies for clients in Bangalore.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Implement digital marketing campaigns in Bangalore.'}
        ],
        ('freelance', 'marketing', 'Mumbai'): [
        {'title': 'Freelance Marketing Consultant', 'description': 'Develop marketing strategies for clients in Mumbai.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Implement digital marketing campaigns in Mumbai.'}
        ],
        ('freelance', 'marketing', 'Pune'): [
        {'title': 'Freelance Marketing Consultant', 'description': 'Develop marketing strategies for clients in Pune.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Implement digital marketing campaigns in Pune.'}
        ],
        ('freelance', 'marketing', 'Delhi'): [
        {'title': 'Freelance Marketing Consultant', 'description': 'Develop marketing strategies for clients in Delhi.'},
        {'title': 'Digital Marketing Specialist', 'description': 'Implement digital marketing campaigns in Delhi.'}
        ],
        ('freelance', 'web-development', 'Bangalore'): [
        {'title': 'Freelance Web Developer', 'description': 'Develop custom web applications in Bangalore.'},
        {'title': 'Front-End Freelancer', 'description': 'Create responsive front-end designs in Bangalore.'}
        ],
        ('freelance', 'web-development', 'Mumbai'): [
        {'title': 'Freelance Web Developer', 'description': 'Develop custom web applications in Mumbai.'},
        {'title': 'Front-End Freelancer', 'description': 'Create responsive front-end designs in Mumbai.'}
        ],
        ('freelance', 'web-development', 'Pune'): [
        {'title': 'Freelance Web Developer', 'description': 'Develop custom web applications in Pune.'},
        {'title': 'Front-End Freelancer', 'description': 'Create responsive front-end designs in Pune.'}
        ],
        ('freelance', 'web-development', 'Delhi'): [
        {'title': 'Freelance Web Developer', 'description': 'Develop custom web applications in Delhi.'},
        {'title': 'Front-End Freelancer', 'description': 'Create responsive front-end designs in Delhi.'}
        ],
         ('freelance', 'graphic-design', 'Bangalore'): [
        {'title': 'Freelance Graphic Designer', 'description': 'Create stunning visual content for clients in Bangalore.'},
        {'title': 'UI/UX Designer', 'description': 'Design intuitive user interfaces and experiences in Bangalore.'}
        ],
        ('freelance', 'graphic-design', 'Mumbai'): [
        {'title': 'Freelance Graphic Designer', 'description': 'Create stunning visual content for clients in Mumbai.'},
        {'title': 'UI/UX Designer', 'description': 'Design intuitive user interfaces and experiences in Mumbai.'}
        ],
        ('freelance', 'graphic-design', 'Pune'): [
        {'title': 'Freelance Graphic Designer', 'description': 'Create stunning visual content for clients in Pune.'},
        {'title': 'UI/UX Designer', 'description': 'Design intuitive user interfaces and experiences in Pune.'}
        ],
        ('freelance', 'graphic-design', 'Delhi'): [
        {'title': 'Freelance Graphic Designer', 'description': 'Create stunning visual content for clients in Delhi.'},
        {'title': 'UI/UX Designer', 'description': 'Design intuitive user interfaces and experiences in Delhi.'}
        ],
        ('internship', 'graphic-design', 'Bangalore'): [
        {'title': 'Graphic Design Intern', 'description': 'Assist senior designers in project execution in Bangalore.'},
        {'title': 'Junior Graphic Designer Intern', 'description': 'Learn and contribute to graphic design projects in Bangalore.'}
        ],
        ('internship', 'graphic-design', 'Mumbai'): [
        {'title': 'Graphic Design Intern', 'description': 'Assist senior designers in project execution in Mumbai.'},
        {'title': 'Junior Graphic Designer Intern', 'description': 'Learn and contribute to graphic design projects in Mumbai.'}
        ],
        ('internship', 'graphic-design', 'Pune'): [
        {'title': 'Graphic Design Intern', 'description': 'Assist senior designers in project execution in Pune.'},
        {'title': 'Junior Graphic Designer Intern', 'description': 'Learn and contribute to graphic design projects in Pune.'}
        ],
        ('internship', 'graphic-design', 'Delhi'): [
        {'title': 'Graphic Design Intern', 'description': 'Assist senior designers in project execution in Delhi.'},
        {'title': 'Junior Graphic Designer Intern', 'description': 'Learn and contribute to graphic design projects in Delhi.'}
        ],
        ('internship', 'web-development', 'Bangalore'): [
        {'title': 'Web Development Intern', 'description': 'Work on web development projects under guidance in Bangalore.'},
        {'title': 'Front-End Development Intern', 'description': 'Learn front-end development skills and apply them in Bangalore.'}
        ],
        ('internship', 'web-development', 'Mumbai'): [
        {'title': 'Web Development Intern', 'description': 'Work on web development projects under guidance in Mumbai.'},
        {'title': 'Front-End Development Intern', 'description': 'Learn front-end development skills and apply them in Mumbai.'}
        ],
        ('internship', 'web-development', 'Pune'): [
        {'title': 'Web Development Intern', 'description': 'Work on web development projects under guidance in Pune.'},
        {'title': 'Front-End Development Intern', 'description': 'Learn front-end development skills and apply them in Pune.'}
        ],
        ('internship', 'web-development', 'Delhi'): [
        {'title': 'Web Development Intern', 'description': 'Work on web development projects under guidance in Delhi.'},
        {'title': 'Front-End Development Intern', 'description': 'Learn front-end development skills and apply them in Delhi.'}
        ],
        ('internship', 'marketing', 'Bangalore'): [
        {'title': 'Marketing Intern', 'description': 'Assist in executing marketing campaigns in Bangalore.'},
        {'title': 'Social Media Intern', 'description': 'Manage social media accounts and campaigns in Bangalore.'}
        ],
        ('internship', 'marketing', 'Mumbai'): [
        {'title': 'Marketing Intern', 'description': 'Assist in executing marketing campaigns in Mumbai.'},
        {'title': 'Social Media Intern', 'description': 'Manage social media accounts and campaigns in Mumbai.'}
        ],
        ('internship', 'marketing', 'Pune'): [
        {'title': 'Marketing Intern', 'description': 'Assist in executing marketing campaigns in Pune.'},
        {'title': 'Social Media Intern', 'description': 'Manage social media accounts and campaigns in Pune.'}
        ],
        ('internship', 'marketing', 'Delhi'): [
        {'title': 'Marketing Intern', 'description': 'Assist in executing marketing campaigns in Delhi.'},
        {'title': 'Social Media Intern', 'description': 'Manage social media accounts and campaigns in Delhi.'}
        ],
        ('internship', 'data-science', 'Bangalore'): [
        {'title': 'Data Science Intern', 'description': 'Analyze datasets and assist in data-driven projects in Bangalore.'},
        {'title': 'Machine Learning Intern', 'description': 'Learn and apply machine learning algorithms in Bangalore.'}
        ],
        ('internship', 'data-science', 'Mumbai'): [
        {'title': 'Data Science Intern', 'description': 'Analyze datasets and assist in data-driven projects in Mumbai.'},
        {'title': 'Machine Learning Intern', 'description': 'Learn and apply machine learning algorithms in Mumbai.'}
        ],
        ('internship', 'data-science', 'Pune'): [
        {'title': 'Data Science Intern', 'description': 'Analyze datasets and assist in data-driven projects in Pune.'},
        {'title': 'Machine Learning Intern', 'description': 'Learn and apply machine learning algorithms in Pune.'}
        ],
        ('internship', 'data-science', 'Delhi'): [
        {'title': 'Data Science Intern', 'description': 'Analyze datasets and assist in data-driven projects in Delhi.'},
        {'title': 'Machine Learning Intern', 'description': 'Learn and apply machine learning algorithms in Delhi.'}
        ],
       
    }
    

    job_descriptions = job_data.get((job_type, domain, location), [])

    return render(request, 'jobs/job_search_results.html', {'job_descriptions': job_descriptions})


def job_search_results(request):
    job_descriptions = request.session.get('job_descriptions', [])
    return render(request, 'jobs/job_search_results.html', {'job_descriptions': job_descriptions})


def application_success(request):
    return render(request, 'jobs/application_success.html')


def employer_dashboard(request):
    return render(request, 'jobs/employer_dashboard.html')


def employer_search(request):
    job_applications = JobApplication.objects.all()
    print(f"Initial count: {job_applications.count()}")

    for app in job_applications:
        print(f"Job Title: {app.job_title}, Description: {app.job_description}")

    return render(request, 'jobs/employer_search_results.html', {
        'job_applications': job_applications,
        'search_params': {
            'job_description': request.GET.get('job_description', ''),
            'location': request.GET.get('location', ''),
        }
    })


def download_resume(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    resume = application.applicant_resume
    if not resume:
        raise Http404("Resume not found")
    response = FileResponse(resume, as_attachment=True, filename=resume.name)
    return response


def post_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_posted_success')  
    else:
        form = JobPostingForm()

    return render(request, 'jobs/post_job.html', {'form': form})


def job_posted_success(request):
    return render(request, 'jobs/job_posted_success.html')





