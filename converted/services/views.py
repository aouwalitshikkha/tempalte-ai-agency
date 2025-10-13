from django.shortcuts import render
from .models import MainService, CompanyLogo, Testimonial,Testimonial

def home(request):
    main_services = MainService.objects.filter(is_active=True).order_by('ranking')
    company_logos = CompanyLogo.objects.all()
    testimonials = Testimonial.objects.filter(show_on_home=True, is_active=True).order_by('ranking')

    context = {
        'main_services': main_services,
        'company_logos': company_logos,
        'testimonials': testimonials,
    }
    return render(request, 'services/home.html', context)

