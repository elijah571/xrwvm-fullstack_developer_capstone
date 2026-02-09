import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CarMake, CarModel, Dealer, Review
from .populate import initiate_cars, initiate_dealers


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
            return JsonResponse({"userName": username, "status": True})

    return JsonResponse({"status": False})


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
        return JsonResponse({"userName": username, "status": True})


# ---------------- CARS ----------------

def get_cars(request):
    initiate_cars()
    cars = CarModel.objects.select_related("car_make")

    data = [
        {
            "CarModel": car.name,
            "CarMake": car.car_make.name,
            "DealerID": car.dealer_id,
            "Type": car.type,
            "Year": car.year,
        }
        for car in cars
    ]

    return JsonResponse({"CarModels": data})


# ---------------- DEALERS ----------------

def get_dealers(request):
    initiate_dealers()
    dealers = Dealer.objects.all().values("id", "full_name", "city", "address", "zip", "state")
    return JsonResponse({"status": 200, "dealers": list(dealers)})


def get_dealers_by_state(request, state):
    if state == "All":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(state=state)

    dealers = dealers.values("id", "full_name", "city", "address", "zip", "state")
    return JsonResponse({"status": 200, "dealers": list(dealers)})


def get_dealer(request, id):
    dealer = Dealer.objects.filter(id=id).values("id", "full_name", "city", "address", "zip", "state")
    return JsonResponse({"status": 200, "dealer": list(dealer)})


def get_reviews(request, id):
    reviews = Review.objects.filter(dealership=id).values(
        "name", "review", "car_make", "car_model", "car_year", "sentiment"
    )
    return JsonResponse({"status": 200, "reviews": list(reviews)})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Review.objects.create(
            name=data["name"],
            dealership=data["dealership"],
            review=data["review"],
            car_make=data["car_make"],
            car_model=data["car_model"],
            car_year=data["car_year"],
            sentiment="positive"
        )

        return JsonResponse({"status": 200})

    return JsonResponse({"status": 400})
