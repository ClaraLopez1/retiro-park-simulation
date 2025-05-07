import matplotlib

matplotlib.use("TkAgg")
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DB_PATH = "../retiro.db"
CLOSING_TIME = pd.to_datetime("22:00", format="%H:%M")


def load_visitors():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM visitors", conn)
    return df


def plot_exit_delay_after_closing():
    df = load_visitors()
    if df.empty:
        print("No visitor data found.")
        return

    df["exit_time"] = pd.to_datetime(df["exit_time"], format="%H:%M", errors="coerce")
    df = df[df["exit_time"].notnull()]

    after_closing = df[df["exit_time"] > CLOSING_TIME].copy()
    after_closing["delay_minutes"] = (after_closing["exit_time"] - CLOSING_TIME).dt.total_seconds() / 60

    if after_closing.empty:
        print("No visitors left after closing time.")
        return

    # Convert exit times to string for x-axis labels
    after_closing["exit_label"] = after_closing["exit_time"].dt.strftime("%H:%M")

    # Sort by exit time
    after_closing = after_closing.sort_values("exit_time")

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(after_closing["exit_label"], after_closing["delay_minutes"], color="tomato", edgecolor="black")

    for bar, mins in zip(bars, after_closing["delay_minutes"]):
        label = f"{int(mins // 60)}h {int(mins % 60)}m" if mins >= 60 else f"{int(mins)}m"
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 label, ha='center', va='bottom', fontsize=9)

    plt.title("Exit Times After Park Closure (22:00)", fontsize=16, fontweight="bold")
    plt.xlabel("Actual Exit Time", fontsize=12)
    plt.ylabel("Delay (Minutes)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle="--", alpha=0.6)
    # Annotate number of late visitors
    total_late = len(after_closing)
    plt.text(0.4, -0.2,
             f"Total late visitors: {total_late}",
             transform=plt.gca().transAxes,
             fontsize=10, color="dimgray", ha="left", va="bottom",
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.show()

    avg_delay = after_closing["delay_minutes"].mean()
    max_delay = after_closing["delay_minutes"].max()

    def format_minutes(m):
        hours = int(m // 60)
        minutes = int(m % 60)
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    print("🔎 Statistics for Visitors Who Left After 22:00")
    print(f"- Average delay: {format_minutes(avg_delay)}")
    print(f"- Maximum delay: {format_minutes(max_delay)}")
    print(f"- Total late visitors: {len(after_closing)}")



def plot_average_stay_duration():
    df = load_visitors()
    if df.empty:
        print("No visitor data found.")
        return

    df["entry_time"] = pd.to_datetime(df["entry_time"], format="%H:%M", errors="coerce")
    df["exit_time"] = pd.to_datetime(df["exit_time"], format="%H:%M", errors="coerce")
    df = df[df["entry_time"].notnull() & df["exit_time"].notnull()]

    # Convert to hours
    df["stay_duration"] = (df["exit_time"] - df["entry_time"]).dt.total_seconds() / 3600  # in hours

    plt.figure(figsize=(10, 6))
    plt.hist(df["stay_duration"], bins=20, color="skyblue", edgecolor="black")
    plt.title("Visitor Stay Duration", fontsize=16, fontweight="bold")
    plt.xlabel("Duration (hours)", fontsize=12)
    plt.ylabel("Number of Visitors", fontsize=12)
    plt.grid(axis='y', linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    # Format duration nicely
    def format_hours(h):
        whole = int(h)
        minutes = int((h - whole) * 60)
        return f"{whole}h {minutes}m" if whole > 0 else f"{minutes}m"

    avg = df['stay_duration'].mean()
    max_dur = df['stay_duration'].max()
    min_dur = df['stay_duration'].min()

    print("🔎 Visitor Stay Duration Stats:")
    print(f"- Average stay: {format_hours(avg)}")
    print(f"- Max stay: {format_hours(max_dur)}")
    print(f"- Min stay: {format_hours(min_dur)}")



if __name__ == "__main__":
    plot_exit_delay_after_closing()
    plot_average_stay_duration()
