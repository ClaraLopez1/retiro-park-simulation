import matplotlib
matplotlib.use("TkAgg")  # Soluciona el error del backend en PyCharm
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

DB_PATH = "../retiro.db"
def load_cafe_orders():
    with sqlite3.connect("../retiro.db") as conn:
        df = pd.read_sql_query("SELECT * FROM cafe_orders", conn)
    return df


def plot_total_revenue_by_cafe():
    df = load_cafe_orders()
    revenue = df.groupby("cafe_name")["item_price"].sum()
    revenue.plot(kind="bar", color="goldenrod", edgecolor="black")
    plt.title("Total Revenue per Café")
    plt.ylabel("Revenue (€)")
    plt.xlabel("Café")
    plt.tight_layout()
    plt.show()

def plot_total_items_sold_by_cafe():
    df = load_cafe_orders()
    counts = df["cafe_name"].value_counts()
    counts.plot(kind="bar", color="salmon", edgecolor="black")
    plt.title("Total Items Sold per Café")
    plt.ylabel("Items Sold")
    plt.xlabel("Café")
    plt.tight_layout()
    plt.show()
def plot_average_spend_by_cafe():
    df = load_cafe_orders()
    avg_spend = df.groupby("cafe_name")["item_price"].mean()
    avg_spend.plot(kind="bar", color="mediumseagreen", edgecolor="black")
    plt.title("Average Spend per Order by Café")
    plt.ylabel("Average (€)")
    plt.xlabel("Café")
    plt.tight_layout()
    plt.show()
def plot_top_items_per_cafe():
    df = load_cafe_orders()
    for cafe in df["cafe_name"].unique():
        cafe_df = df[df["cafe_name"] == cafe]
        item_counts = cafe_df["item_name"].value_counts().head(5)

        plt.figure(figsize=(8, 4))
        item_counts.plot(kind="bar", color="cornflowerblue", edgecolor="black")
        plt.title(f"Top-Selling Items - {cafe}")
        plt.ylabel("Units Sold")
        plt.xlabel("Item")
        plt.tight_layout()
        plt.show()
def plot_top_buyers_per_cafe():
    df = load_cafe_orders()
    for cafe in df["cafe_name"].unique():
        cafe_df = df[df["cafe_name"] == cafe]
        top_buyers = cafe_df["visitor_id"].value_counts().head(5)

        plt.figure(figsize=(8, 4))
        top_buyers.plot(kind="bar", color="orchid", edgecolor="black")
        plt.title(f"Top Buyers - {cafe}")
        plt.ylabel("Orders")
        plt.xlabel("Visitor ID")
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    plot_total_revenue_by_cafe()
    plot_total_items_sold_by_cafe()
    plot_average_spend_by_cafe()
    plot_top_items_per_cafe()
    plot_top_buyers_per_cafe()