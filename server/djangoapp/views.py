import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CarMake, CarModel, Dealer, Review
from .populate import initiate_cars, initiate_dealers, initiate_reviews
from datetime import date

# ---------------- AUTH ----------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"status": "Failed"})


def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


# ---------------- CARS ----------------
def get_cars(request):
    initiate_cars()
    cars = CarModel.objects.select_related("car_make", "dealer")
    data = [
        {
            "CarMake": car.car_make.name,
            "CarModel": car.name,
            "Dealer": car.dealer.full_name,
            "Type": car.type,
            "Year": car.year
        }
        for car in cars
    ]
    return JsonResponse({"CarModels": data})


# ---------------- DEALERS ----------------
def get_dealer(request, dealer_id):
    dealer = Dealer.objects.filter(id=dealer_id).values(
        "id", "full_name", "city", "state", "address", "zip"
    ).first()
    return JsonResponse({"dealer": dealer})


def get_dealers_by_state(request, state):
    if state.lower() == "all":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(state__iexact=state)
    dealers = dealers.values("id", "full_name", "city", "state", "address", "zip")
    return JsonResponse({"dealers": list(dealers)})


def get_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealership_id=dealer_id).values(
        "name", "review", "car_make", "car_model", "car_year", "purchase_date", "sentiment"
    )
    return JsonResponse({"dealer_id": dealer_id, "reviews": list(reviews)})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        dealer_obj = Dealer.objects.get(id=data["dealership"])
        Review.objects.create(
            name=data["name"],
            dealership=dealer_obj,
            review=data["review"],
            car_make=data["car_make"],
            car_model=data["car_model"],
            car_year=data["car_year"],
            sentiment="positive",
            purchase_date=data.get("purchase_date", date.today())
        )
        return JsonResponse({"status": "Review Added"})
    return JsonResponse({"status": "Failed"})

@csrf_exempt
def analyze_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get("review", "")
        sentiment = (
            "positive"
            if any(word in review_text.lower() for word in ["good", "great", "fantastic"])
            else "neutral"
        )
        return JsonResponse({"review": review_text, "sentiment": sentiment})
    return JsonResponse({"status": "Failed"})
