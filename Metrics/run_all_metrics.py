from visitors_metrics import (
    plot_exit_delay_after_closing,
    plot_average_stay_duration,
    plot_avg_stay_by_persona,
    plot_entry_time_distribution,
    plot_exit_time_distribution,
)

from sport_metrics import (
    plot_total_games_per_sport,
    plot_avg_duration_per_sport,
    plot_top_players,
)

from cafe_metrics import (
    plot_total_revenue_by_cafe,
    plot_total_items_sold_by_cafe,
    plot_average_spend_by_cafe,
    plot_top_items_per_cafe,
    plot_top_buyers_per_cafe,
)

from activity_metrics import (
    plot_activity_count_by_hour,
    plot_top_activities,
    plot_most_common_activity_per_hour,
    plot_top_monuments,
    # Optional if too many: plot_activity_distribution_per_hour, plot_top_activities_by_visitor
)


def run_all():
    # Visitor metrics
    plot_exit_delay_after_closing()
    plot_average_stay_duration()
    plot_avg_stay_by_persona()
    plot_entry_time_distribution()
    plot_exit_time_distribution()

    # Sports metrics
    plot_total_games_per_sport()
    plot_avg_duration_per_sport()
    plot_top_players()

    # Café metrics
    plot_total_revenue_by_cafe()
    plot_total_items_sold_by_cafe()
    plot_average_spend_by_cafe()
    plot_top_items_per_cafe()
    plot_top_buyers_per_cafe()

    # Activity metrics
    plot_activity_count_by_hour()
    plot_top_activities()
    plot_most_common_activity_per_hour()
    plot_top_monuments()


if __name__ == "__main__":
    run_all()
