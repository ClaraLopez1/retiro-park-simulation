import time

_time_manager = None

def set_time_manager(time_manager):
    global _time_manager
    _time_manager = time_manager

def log(message):
    if _time_manager:
        current_time = _time_manager.get_current_time()
    else:
        current_time = time.strftime("%H:%M:%S")  # fallback
    print(f"[{current_time}] {message}", flush=True)