from django.shortcuts import render


def render_react(request):
    """
    Main View to render all of REACT app
    """
    return render(request, "index.html")
