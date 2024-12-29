from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # Ensure xhtml2pdf is installed
from events.models import Event
from products.models import EventProduct
from datetime import datetime


# Product Form View
def product_form(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
    else:
        product = None

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product saved successfully!")
            return redirect("products:product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {"form": form})

# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("products:product_list")


def product_order(request, event_id):
    """
    Generate and manage the purchase order for an event's products.
    """
    event = get_object_or_404(Event, id=event_id)
    event_products = EventProduct.objects.filter(event=event)

    if request.method == "POST":
        # Update overridden quantities
        for product in event_products:
            field_name = f"quantity_{product.id}"
            if field_name in request.POST:
                new_quantity = request.POST.get(field_name, product.quantity)
                product.quantity = int(new_quantity)
                product.save()

        # Generate PDF after form submission
        return generate_purchase_order_pdf(event)

    # Pass data to the template
    return render(request, "products/product_order.html", {
        "event": event,
        "event_products": event_products,
    })


def generate_purchase_order_pdf(event):
    """
    Generate a PDF of the purchase order.
    """
    event_products = EventProduct.objects.filter(event=event)
    template = get_template("products/purchase_order_pdf.html")
    context = {
        "event": event,
        "event_products": event_products,
        "current_year": datetime.now().year,
    }
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="purchase_order_event_{event.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF <pre>" + html + "</pre>")
    return response
