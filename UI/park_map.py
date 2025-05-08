import random

ALLOWED_BOUNDS = {
    "renting a Boat": {"x": (360, 630), "y": (450, 590)},
    "Football 7v7": {"x": (875, 975), "y": (630, 670)},
    "Padel": {"x": (875, 935), "y": (685, 715)},
    "Tennis": {"x": (950, 975), "y": (685, 730)},
    "🏛️ visiting Palacio de Cristal": {"x": (860, 990), "y": (410, 470)},
    "🖼 visiting Palacio de Velazquez": {"x": (670, 810), "y": (320, 380)},
    "renting a Bike": {"x": (900, 930), "y": (300, 330)},
    "visiting StarCafe": {"x": (400, 420), "y": (180, 200)},
    "visiting RetiroBistro": {"x": (170, 190), "y": (320, 340)},
    "🗿 visiting Angel Caido": {"x": (1040, 1060), "y": (590, 610)},
}

def is_inside_bounds(x, y, bounds):
    return bounds["x"][0] <= x <= bounds["x"][1] and bounds["y"][0] <= y <= bounds["y"][1]


def get_safe_coord(area_bounds):
    max_attempts = 50
    for _ in range(max_attempts):
        x = random.randint(*area_bounds["x"])
        y = random.randint(*area_bounds["y"])
        if not any(is_inside_bounds(x, y, b) for b in ALLOWED_BOUNDS.values()):
            return (x, y)
    return (700, 500)  # fallback


def get_activity_coord(activity_name):
    if activity_name == "🚶‍ walking":
        walking_bounds = {"x": (150, 1200), "y": (150, 850)}
        return get_safe_coord(walking_bounds)

    if activity_name == "🎭 watching a Street Performance":
        street_bounds = {"x": (100, 600), "y": (200, 500)}
        return get_safe_coord(street_bounds)

    if activity_name == "📸 taking Photos":
        photo_bounds = {"x": (150, 900), "y": (150, 650)}
        return get_safe_coord(photo_bounds)

    if activity_name == "🏃 running":
        running_bounds = {"x": (300, 1100), "y": (700, 850)}
        return get_safe_coord(running_bounds)

    if activity_name in ALLOWED_BOUNDS:
        x_min, x_max = ALLOWED_BOUNDS[activity_name]["x"]
        y_min, y_max = ALLOWED_BOUNDS[activity_name]["y"]
        return (random.randint(x_min, x_max), random.randint(y_min, y_max))

    return (700, 500)  # fallback



