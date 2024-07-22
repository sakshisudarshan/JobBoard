from django import forms
from .models import JobApplication, JobPosting

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job_title', 'job_description', 'applicant_resume']

    def save(self, commit=True):
        job_application = super(JobApplicationForm, self).save(commit=False)
        
        if commit:
            job_application.save()
        return job_application


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_title', 'job_description', 'job_type', 'domain', 'location']
