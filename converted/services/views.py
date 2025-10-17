from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Contact

def home(request):
    services = Service.objects.all().order_by('service_name')
    country = request.META.get('HTTP_CF_IPCOUNTRY', 'XX')  # 'XX' = unknown
    if country == 'BD':  # 🇧🇩 Bangladesh
        whatsapp_no = '+8801790007709'
    else:
        whatsapp_no = 'JinnatVai'
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        company = request.POST.get("company")
        message_text = request.POST.get("message")
        service_id = request.POST.get("service_interested")

        Contact.objects.create(
            name=name,
            email=email,
            company=company,
            service_interested_id=service_id if service_id else None,
            page_source="Homepage Contact Form",
            page_url=request.build_absolute_uri(),
            message=message_text,
        )

        messages.success(request, "Thank you for your message! We will get back to you soon.")

        referer_url = request.META.get("HTTP_REFERER", "/")
        redirect_url = f"{referer_url.split('#' )[0]}#contact"
        
        return redirect(redirect_url)

    context = {
        "services": services,
        'whatsapp_no':whatsapp_no
    }
    return render(request, "services/home.html", context)




def service_detail(request, slug):
    """
    Display a single service with its details (hero area + short details + bullet points).
    """
    # Optimize database queries:
    # - select_related: joins the 1-to-1 ServiceDetails table
    # - prefetch_related: fetches all BulletPoints in one go
    service = get_object_or_404(
        Service.objects.select_related("details").prefetch_related("details__bullet_points"),
        slug=slug
    )

    context = {
        "service": service,
        "details": service.details,  # for convenience in template
        "bullet_points": service.details.bullet_points.all(),
    }
    return render(request, "services/service_detail.html", context)