from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Contact, FAQ, SubService

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




def subservice_detail(request, service_slug, subservice_slug):
    """
    Display a SubService detail page based on nested slugs:
    /<service>/<subservice>/
    """

    # Ensure both service and sub-service exist and match
    parent_service = get_object_or_404(Service, slug=service_slug, is_active=True)
    sub_service = get_object_or_404(
        SubService,
        slug=subservice_slug,
        parent_service=parent_service,
        is_active=True,
    )

    # Related subservices (for sidebar/navigation)
    related_subservices = (
        parent_service.sub_services.filter(is_active=True)
        .exclude(id=sub_service.id)
        .order_by("order")
    )

    # Features
    features = sub_service.features.all()

    # FAQs: Prefer sub-service ones, fallback to parent service
    faqs = FAQ.objects.filter(is_active=True, sub_service=sub_service)
    if not faqs.exists():
        faqs = FAQ.objects.filter(is_active=True, service=parent_service)

    context = {
        "sub_service": sub_service,
        "parent_service": parent_service,
        "related_subservices": related_subservices,
        "features": features,
        "faqs": faqs,
    }

    return render(request, "services/subservice_detail.html", context)