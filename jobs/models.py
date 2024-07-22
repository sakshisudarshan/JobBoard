from django.db import models

class JobApplication(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    applicant_resume = models.FileField(upload_to='resumes/%Y/%m/%d/')

    def __str__(self):
        return f'{self.job_title} Application'
    

class JobPosting(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_type = models.CharField(max_length=100, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Freelance', 'Freelance'),('Internship','Internship')])
    domain = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title



