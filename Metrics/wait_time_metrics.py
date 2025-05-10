from datetime import datetime, timedelta
import matplotlib
matplotlib.use("TkAgg")

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "../retiro.db"

SIM_START_SIM = datetime.strptime("06:00:00", "%H:%M:%S")
SIM_START_REAL = None  # Global reference for first real-world timestamp


def real_to_sim_time(real_time):
    global SIM_START_REAL
    if SIM_START_REAL is None:
        SIM_START_REAL = real_time
        return SIM_START_SIM

    elapsed = (real_time - SIM_START_REAL).total_seconds()
    sim_minutes = int(elapsed * 5)
    return SIM_START_SIM + timedelta(minutes=sim_minutes)


def load_sport_wait_times():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sport_wait_times", conn)
    conn.close()

    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format="%H:%M:%S")
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M:%S")
    df["wait_duration"] = df["wait_duration"].astype(int) * 5

    df["simulated_arrival"] = df["arrival_time"].apply(real_to_sim_time)
    df["sim_hour"] = df["simulated_arrival"].dt.hour

    return df


def load_cafe_wait_times():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cafe_wait_times", conn)
    conn.close()

    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format="%H:%M:%S")
    df["wait_duration"] = df["wait_duration"].astype(int) * 5

    df["simulated_arrival"] = df["arrival_time"].apply(real_to_sim_time)
    df["sim_hour"] = df["simulated_arrival"].dt.hour

    return df


def load_boat_wait_times():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM boat_wait_times", conn)
    conn.close()

    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format="%H:%M:%S")
    df["wait_duration"] = df["wait_duration"].astype(int) * 5

    df["simulated_arrival"] = df["arrival_time"].apply(real_to_sim_time)
    df["sim_hour"] = df["simulated_arrival"].dt.hour

    return df


def load_bike_wait_times():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM bike_wait_times", conn)
    conn.close()

    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format="%H:%M:%S")
    df["wait_duration"] = df["wait_duration"].astype(int) * 5

    df["simulated_arrival"] = df["arrival_time"].apply(real_to_sim_time)
    df["sim_hour"] = df["simulated_arrival"].dt.hour

    return df


def plot_avg_wait_time_per_sport_by_hour():
    df = load_sport_wait_times()
    grouped = df.groupby(["sim_hour", "sport_name"]).wait_duration.mean().unstack().fillna(0)
    grouped.plot(kind="line", marker='o', figsize=(10, 6))
    plt.title("⏳ Average Wait Time per Sport by Simulated Hour")
    plt.xlabel("Simulated Hour (e.g., 6 = 6AM)")
    plt.ylabel("Average Wait Time (minutes)")
    plt.xticks(ticks=range(6, 23), labels=[f"{h}:00" for h in range(6, 23)])
    plt.grid(True)
    plt.legend(title="Sport")
    plt.tight_layout()
    plt.show()


def plot_avg_wait_time_per_cafe_by_hour():
    df = load_cafe_wait_times()
    grouped = df.groupby(["sim_hour", "cafe_name"]).wait_duration.mean().unstack().fillna(0)
    grouped.plot(kind="line", marker='o', figsize=(10, 6))
    plt.title("☕ Average Wait Time per Café by Simulated Hour")
    plt.xlabel("Simulated Hour (e.g., 6 = 6AM)")
    plt.ylabel("Average Wait Time (minutes)")
    plt.xticks(ticks=range(6, 23), labels=[f"{h}:00" for h in range(6, 23)])
    plt.grid(True)
    plt.legend(title="Café")
    plt.tight_layout()
    plt.show()


def plot_avg_wait_time_per_boat_by_hour():
    df = load_boat_wait_times()
    grouped = df.groupby("sim_hour").wait_duration.mean()
    grouped.plot(kind="line", marker='o', figsize=(10, 5), color="navy")
    plt.title("🚣 Average Wait Time for Boat Rentals by Simulated Hour")
    plt.xlabel("Simulated Hour (e.g., 6 = 6AM)")
    plt.ylabel("Average Wait Time (minutes)")
    plt.xticks(ticks=range(6, 23), labels=[f"{h}:00" for h in range(6, 23)])
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_avg_wait_time_per_bike_by_hour():
    df = load_bike_wait_times()
    grouped = df.groupby("sim_hour").wait_duration.mean()
    grouped.plot(kind="line", marker='o', figsize=(10, 5), color="green")
    plt.title("🚴 Average Wait Time for Bike Rentals by Simulated Hour")
    plt.xlabel("Simulated Hour (e.g., 6 = 6AM)")
    plt.ylabel("Average Wait Time (minutes)")
    plt.xticks(ticks=range(6, 23), labels=[f"{h}:00" for h in range(6, 23)])
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_avg_wait_time_per_cafe_by_hour()
    plot_avg_wait_time_per_sport_by_hour()
    plot_avg_wait_time_per_boat_by_hour()
    plot_avg_wait_time_per_bike_by_hour()
