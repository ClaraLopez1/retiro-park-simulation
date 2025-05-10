import matplotlib
matplotlib.use("TkAgg")  # Soluciona el error del backend en PyCharm
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

DB_PATH = "../retiro-park-simulation/retiro.db"

def load_activities():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM activities", conn)
    return df

def plot_activity_count_by_hour():
    df = load_activities()

    if df.empty:
        print("No activity data found.")
        return

    # Parseo correcto del timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%H:%M", errors="coerce")
    df["hour"] = df["timestamp"].dt.hour

    grouped = df.groupby(["hour", "activity_name"]).size().unstack(fill_value=0)

    num_activities = grouped.shape[1]
    colors = cm.get_cmap("tab20", num_activities).colors  # hasta 20 colores bien diferenciados

    plt.figure(figsize=(14, 6))
    ax = grouped.plot(kind="line", marker="o", color=colors, linewidth=2, ax=plt.gca())

    plt.title("Activity per Hour of the Day", fontsize=16)
    plt.xlabel("Hour of Day", fontsize=12)
    plt.ylabel("Number of Activities", fontsize=12)
    plt.xticks(np.arange(6, 23, 1))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(title="Activity", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()

def plot_top_activities():
    df = load_activities()

    if df.empty:
        print("No activity data found.")
        return

    counts = df["activity_name"].value_counts().head(10)
    counts.plot(kind="barh", color="skyblue")
    plt.title("Top 10 actividades más realizadas")
    plt.xlabel("Cantidad")
    plt.tight_layout()
    plt.show()

def plot_activity_distribution_per_hour():
    df = load_activities()
    if df.empty:
        print("No activity data found.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%H:%M", errors="coerce")
    df = df[df["timestamp"].notnull()]
    df["hour"] = df["timestamp"].dt.hour

    for activity in df["activity_name"].unique():
        activity_df = df[df["activity_name"] == activity]
        counts = activity_df["hour"].value_counts().sort_index()

        plt.figure(figsize=(10, 4))
        counts.plot(kind="bar", color="mediumseagreen", edgecolor="black")
        plt.title(f"Hourly Distribution - {activity}")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Occurrences")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()

def plot_most_common_activity_per_hour():
    df = load_activities()
    if df.empty:
        print("No activity data found.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%H:%M", errors="coerce")
    df = df[df["timestamp"].notnull()]
    df["hour"] = df["timestamp"].dt.hour

    most_common = df.groupby("hour")["activity_name"].agg(lambda x: x.value_counts().idxmax())

    plt.figure(figsize=(14, 6))
    most_common.value_counts().plot(kind="bar", color="lightcoral", edgecolor="black")
    plt.title("Most Frequent Activity per Hour (Overall)")
    plt.xlabel("Activity Name")
    plt.ylabel("Number of Hours it was the Top Activity")
    plt.tight_layout()
    plt.show()

def plot_top_activities_by_visitor():
    df = load_activities()
    if df.empty:
        print("No activity data found.")
        return

    top_visitors = df["visitor_id"].value_counts().head(5).index

    for visitor_id in top_visitors:
        visitor_df = df[df["visitor_id"] == visitor_id]
        counts = visitor_df["activity_name"].value_counts()

        plt.figure(figsize=(8, 4))
        counts.plot(kind="bar", color="steelblue", edgecolor="black")
        plt.title(f"Activity Distribution - Visitor {visitor_id}")
        plt.xlabel("Activity")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

def plot_top_monuments():
    df = load_activities()
    if df.empty:
        print("No activity data available.")
        return

    # Define the list of known monuments
    monuments = ["Palacio de Cristal", "Angel Caido", "Palacio de Velazquez"]
    monument_df = df[df["activity_name"].isin(monuments)]

    if monument_df.empty:
        print("No data found for monument visits.")
        return

    # Count visits and preserve original order
    visit_counts = monument_df["activity_name"].value_counts().reindex(monuments, fill_value=0)

    # Plot configuration
    plt.figure(figsize=(10, 5))
    bars = plt.bar(visit_counts.index, visit_counts.values, color="#FFA500", edgecolor="black")

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 1, str(int(height)),
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Styling
    plt.title("Most Visited Monuments", fontsize=16, fontweight='bold')
    plt.xlabel("Monument", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
     plot_activity_count_by_hour()
     plot_top_activities()
     # plot_activity_distribution_per_hour()
     plot_most_common_activity_per_hour()
     #plot_top_activities_by_visitor()
     plot_top_monuments()


