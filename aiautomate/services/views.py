from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Contact

def home(request):
    services = Service.objects.all().order_by('service_name')

    if request.method == "POST":
        # ... (your form processing logic remains the same)
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

        # --- ✅ SOLUTION ---
        # Get the previous page URL
        referer_url = request.META.get("HTTP_REFERER", "/")
        
        # Append the fragment to scroll to the contact section
        # This ensures we redirect to http://yourdomain.com/#contact
        redirect_url = f"{referer_url.split('#' )[0]}#contact"
        
        return redirect(redirect_url)

    context = {
        "services": services,
    }
    return render(request, "services/home.html", context)
