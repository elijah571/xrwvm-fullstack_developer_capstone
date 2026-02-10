from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    # AUTH
    path("login", views.login_user),
    path("logout", views.logout_user),
    path("register", views.register_user),

    # CARS
    path("get_cars", views.get_cars),

    # DEALERS
    path("fetchDealer/<int:dealer_id>", views.get_dealer),
    path("fetchDealerByState/<str:state>", views.get_dealers_by_state),
    path("fetchReviews/dealer/<int:dealer_id>", views.get_reviews),
    
    # REVIEWS
    path("add_review", views.add_review),
    path("analyzeReview", views.analyze_review),
]
