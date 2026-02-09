from .models import CarMake, CarModel, Dealer, Review


def initiate_cars():
    if CarMake.objects.exists():
        return

    makes = [
        ("NISSAN", "Great cars from Japan"),
        ("Toyota", "Reliable cars"),
        ("Ford", "American cars"),
    ]

    models = [
        ("Pathfinder", 15, "NISSAN", "SUV", 2023),
        ("Altima", 12, "NISSAN", "Sedan", 2022),
        ("Corolla", 10, "Toyota", "Sedan", 2023),
        ("Rav4", 11, "Toyota", "SUV", 2022),
        ("Explorer", 9, "Ford", "SUV", 2023),
        ("Focus", 8, "Ford", "Sedan", 2021),
    ]

    make_objects = {}
    for name, desc in makes:
        make_objects[name] = CarMake.objects.create(name=name, description=desc)

    for name, dealer_id, make_name, car_type, year in models:
        CarModel.objects.create(
            name=name,
            dealer_id=dealer_id,
            car_make=make_objects[make_name],
            type=car_type,
            year=year
        )


def initiate_dealers():
    if Dealer.objects.exists():
        return

    dealers = [
        {"full_name": "Dealer 15", "city": "Los Angeles", "address": "Street 1", "zip": "90001", "state": "California"},
        {"full_name": "Dealer 12", "city": "Houston", "address": "Street 2", "zip": "77001", "state": "Texas"},
        {"full_name": "Dealer 10", "city": "New York", "address": "Street 3", "zip": "10001", "state": "New York"},
        {"full_name": "Dealer 11", "city": "Miami", "address": "Street 4", "zip": "33101", "state": "Florida"},
        {"full_name": "Dealer 9", "city": "Las Vegas", "address": "Street 5", "zip": "88901", "state": "Nevada"},
        {"full_name": "Dealer 8", "city": "Phoenix", "address": "Street 6", "zip": "85001", "state": "Arizona"},
    ]

    for d in dealers:
        Dealer.objects.create(**d)


def initiate_reviews():
    if Review.objects.exists():
        return

    Review.objects.create(
        name="John",
        dealership=1,
        review="Great service!",
        car_make="Toyota",
        car_model="Corolla",
        car_year=2023,
        sentiment="positive"
    )
