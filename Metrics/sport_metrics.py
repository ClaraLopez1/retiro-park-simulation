import matplotlib

matplotlib.use("TkAgg")
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DB_PATH = "../retiro-park-simulation/retiro.db"
def load_sport_games():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM sport_games", conn)
    return df

def plot_total_games_per_sport():
    df = load_sport_games()
    counts = df["sport_name"].value_counts()
    counts.plot(kind="bar", color="steelblue", edgecolor="black")
    plt.title("Total Games per Sport")
    plt.xlabel("Sport")
    plt.ylabel("Number of Games")
    plt.tight_layout()
    plt.show()


def plot_avg_duration_per_sport():
    df = load_sport_games()
    avg_duration = df.groupby("sport_name")["duration"].mean()
    avg_duration.plot(kind="bar", color="orange", edgecolor="black")
    plt.title("Average Game Duration per Sport")
    plt.xlabel("Sport")
    plt.ylabel("Average Duration (minutes)")
    plt.tight_layout()
    plt.show()



def plot_top_players():
    df = load_sport_games()
    from collections import Counter
    all_players = df["player_ids"].str.split(",").explode().astype(int)
    top_players = all_players.value_counts().head(10)

    top_players.plot(kind="bar", color="orchid", edgecolor="black")
    plt.title("Top 10 Most Active Players")
    plt.xlabel("Visitor ID")
    plt.ylabel("Games Played")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_total_games_per_sport()
    plot_avg_duration_per_sport()
    plot_top_players()