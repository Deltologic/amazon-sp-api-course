from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        user = request.user

    else:
        user = None

    return render(request, "lwa_app/index.html", context={user: user})
