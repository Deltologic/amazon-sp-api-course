from django.urls import path
from lwa_app.lwa import (
    begin_oauth,
    oauth_redirect,
    oauth_callback,
    oauth_callback_api,
)

from lwa_app.views import index

urlpatterns = [
    # lwa
    path("", index, name="landing-page"),
    path("lwa/", begin_oauth, name="lwa_begin_oauth"),
    path("lwa/auth", oauth_redirect, name="lwa_redirect"),
    path("lwa/auth/redirect", oauth_callback, name="lwa_callback"),
    path("lwa/finish", oauth_callback_api, name="lwa_callback_api"),
]
