from django.shortcuts import render

def admin(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'admin.html')

