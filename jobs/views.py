from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application


def job_list(request):
    query = request.GET.get('q', '').strip()

    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query
    })


def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'jobs/job_detail.html', {
        'job': job
    })


def apply_job(request, job_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        job = Job.objects.get(id=job_id)

        Application.objects.create(
            job=job,
            name=name,
            email=email
        )

        messages.success(
            request,
            'Application submitted successfully!'
        )

    return render(request, 'jobs/apply.html')