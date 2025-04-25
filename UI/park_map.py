import random

PARK_BOUNDS = {
    "x": (50, 1050),
    "y": (50, 800)
}

# New mapping: specific coordinates for each activity
ACTIVITY_COORDS = {
    #"Renting a Boat": (360, 590),
    "Renting a Bike": (915, 320),
    #"Football 7v7": (925, 650),
    #"Football 13v13": (370, 430),
    #"Padel": (935, 685),
    "Tennis": (975, 730),
    # "Walking": (322, 408), #TODO
    # "Watching a Street Performance": (90, 330), #TODO
    # "Taking Photos": (100, 100), #TODO
    # "Running": (390, 800), #TODO
    "Visiting StarCafe": (410, 190),
    "Visiting RetiroBistro": (180, 330),
    "Angel Caido": (1050, 600),
}

RESTRICTED_ALLOWED_BOUNDS = {
    "Renting a Boat": {"x": (360, 630), "y": (450, 590)},
    "Football 7v7": {"x": (875, 975), "y": (630, 670)},
    #"Football 13v13": {"x": (350, 390), "y": (410, 450)},
    "Padel": {"x": (875, 935), "y": (685, 715)},
    "Tennis": {"x": (950, 975), "y": (685, 730)},
    "Palacio de Cristal": {"x": (860, 990), "y": (410, 470)},
    "Palacio de Velazquez": {"x": (670, 810), "y": (320, 380)},
}

RANDOMIZED_ACTIVITIES = {
    "Walking", "Watching a Street Performance", "Taking Photos", "Running"
}


def is_in_restricted_zone(x, y):
    for bounds in RESTRICTED_ALLOWED_BOUNDS.values():
        if bounds["x"][0] <= x <= bounds["x"][1] and bounds["y"][0] <= y <= bounds["y"][1]:
            return True
    return False


def get_random_safe_coord():
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(*PARK_BOUNDS["x"])
        y = random.randint(*PARK_BOUNDS["y"])
        if not is_in_restricted_zone(x, y):
            return (x, y)
    # fallback
    return (10, 10)


def get_activity_coord(activity_name):
    if activity_name in RESTRICTED_ALLOWED_BOUNDS:
        x_min, x_max = RESTRICTED_ALLOWED_BOUNDS[activity_name]["x"]
        y_min, y_max = RESTRICTED_ALLOWED_BOUNDS[activity_name]["y"]
        return (random.randint(x_min, x_max), random.randint(y_min, y_max))

    if activity_name in RANDOMIZED_ACTIVITIES:
        return get_random_safe_coord()

    return ACTIVITY_COORDS.get(activity_name, (10, 10))


def get_activity_coord(activity_name):
    if activity_name in RESTRICTED_ALLOWED_BOUNDS:
        x_min, x_max = RESTRICTED_ALLOWED_BOUNDS[activity_name]["x"]
        y_min, y_max = RESTRICTED_ALLOWED_BOUNDS[activity_name]["y"]
        return (random.randint(x_min, x_max), random.randint(y_min, y_max))
    return ACTIVITY_COORDS.get(activity_name, (10, 10))
