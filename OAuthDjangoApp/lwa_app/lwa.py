import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from lwa_app.models import AmazonSPAPIConnection
from django.contrib.auth.models import User


# /
def begin_oauth(request):
    return redirect(
        (
                "https://sellercentral.amazon.com/apps/authorize/consent?application_id=%s&state=&redirect_uri="
                % settings.AMAZON_LWA_SOLUTION_ID
        )
        + "&version=beta"  # If public listed app it shouldn't be there
    )


# /auth
def oauth_redirect(request):
    amazon_state = request.GET.get("amazon_state")
    amazon_callback_uri = request.GET.get("amazon_callback_uri")

    return redirect(
        amazon_callback_uri
        + "?amazon_state="
        + amazon_state
        + "&state=&redirect_uri="
        + "&version=beta"
    )


# /auth/redirect
def oauth_callback(request):
    return render(request, "lwa_app/callback.html")


# /finish
def oauth_callback_api(request):
    user = User.objects.get(pk=request.user.pk)
    selling_partner_id = request.GET.get("selling_partner_id")
    spapi_oauth_code = request.GET.get("spapi_oauth_code")

    if selling_partner_id is None or spapi_oauth_code is None:
        raise Exception("Missing selling_partner_id or spapi_oauth_code")

    # https://developer-docs.amazon.com/amazon-shipping/docs/amazon-scpn-authorization-workflow

    credentials = dict(
        refresh_token="",
        lwa_app_id=settings.AMAZON_LWA_APP_ID,
        lwa_client_secret=settings.AMAZON_LWA_CLIENT_SECRET,
    )

    response = requests.post(
        "https://api.amazon.com/auth/o2/token",
        data={
            "grant_type": "authorization_code",
            "code": spapi_oauth_code,
            "client_id": credentials["lwa_app_id"],
            "client_secret": credentials["lwa_client_secret"],
        },
    )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    if not "refresh_token" in data:
        raise Exception("Missing refresh_token")

    AmazonSPAPIConnection.objects.create(
        user=user,
        refresh_token=data["refresh_token"],
    )

    return HttpResponse("SP API authorized successfully!")
