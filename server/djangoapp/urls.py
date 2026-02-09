from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("login", views.login_user),
    path("logout", views.logout_user),
    path("register", views.register_user),

    path("get_cars", views.get_cars),
    path("get_dealers", views.get_dealers),
    path("get_dealers/<str:state>", views.get_dealers_by_state),

    path("dealer/<int:id>", views.get_dealer),
    path("reviews/dealer/<int:id>", views.get_reviews),

    path("add_review", views.add_review),
]
