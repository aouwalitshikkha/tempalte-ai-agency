from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Contact, FAQ

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
    service = get_object_or_404(
        Service.objects
        .select_related("details")
        .prefetch_related(
            "details__bullet_points",
            "sub_services__features"
        ),
        slug=slug
    )

    context = {
        "service": service,
        "details": service.details,
        "bullet_points": service.details.bullet_points.all(),
        "sub_services": service.sub_services.all(),
        # ✅ only FAQs linked *directly* to this main service
        "faqs": FAQ.objects.filter(
            service=service,
            sub_service__isnull=True,
            is_active=True
        ),
    }
    print("Service Detail Context:", context)  # Debugging line
    return render(request, "services/service_detail.html", context)
