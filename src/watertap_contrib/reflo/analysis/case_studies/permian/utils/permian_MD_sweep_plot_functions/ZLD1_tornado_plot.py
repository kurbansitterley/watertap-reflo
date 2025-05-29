import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import math


def tornado_plot(baseline_lcow, df, title="<Low> VS <High> values"):
    """
    Parameters
    ----------
    baseline_lcow: The LCOW assuming baseline costing parameters
    df: Dataframe containing-
        1. Sensitivity parameter labels
        2. Sensitivity parameter baseline price
        2. Low values
        3. High values

    tite: Title of the plot
    """

    color_low = "royalblue"  #'#e1ceff'
    color_high = "darkorange"  # ff6262'

    ys = range(len(df["labels"]))[::1]  # iterate through # of labels

    for y, low_value, high_value in zip(
        ys, df["lcow_low_values"], df["lcow_high_values"]
    ):

        low_width = baseline_lcow - low_value
        high_width = high_value - baseline_lcow

        plt.broken_barh(
            [(low_value, low_width), (baseline_lcow, high_width)],
            (y - 0.4, 0.8),  # thickness of bars and their offset
            facecolors=[color_low, color_high],
            edgecolors=["black", "black"],
            linewidth=1,
        )

        offset = 1  # offset value labels from end of bar

        if high_value > low_value:
            x_high = baseline_lcow + high_width + offset
            x_low = baseline_lcow - low_width - offset
        else:
            x_high = baseline_lcow + high_width - offset
            x_low = baseline_lcow - low_width + offset

        x_low_change = (baseline_lcow - low_value) / baseline_lcow * 100
        x_high_change = (high_value - baseline_lcow) / baseline_lcow * 100

        plt.text(x_high, y + 0.1, str(f"{high_value:0.1f}"), va="center", ha="center")
        plt.text(x_low, y + 0.1, str(f"{low_value:0.1f}"), va="center", ha="center")

        plt.text(
            x_low,
            y - 0.1,
            "(-" + str(f"{x_low_change:0.1f}") + "%)",
            va="center",
            ha="center",
        )
        plt.text(
            x_high,
            y - 0.1,
            "(+" + str(f"{x_high_change:0.1f}") + "%)",
            va="center",
            ha="center",
        )

    plt.axvline(baseline_lcow, ymax=0.7, color="black", linewidth=1)

    plt.text(
        (
            math.floor(min(df["lcow_low_values"]))
            + math.ceil(max(df["lcow_high_values"]))
        )
        / 2,
        len(df["labels"]) + 0.2,
        title,
        va="center",
        ha="center",
        fontdict={"fontsize": 20},
    )

    plt.xlabel("LCOW (\$/m$^3$)")
    plt.yticks(ys, df["labels"], verticalalignment="center")
    plt.ylim(-0.5, len(df["labels"]) + 0.5)
    plt.xticks(np.arange(0, max(df["lcow_high_values"]) + 3, 1))
    plt.xlim(
        math.floor(min(df["lcow_low_values"])) - 2,
        math.ceil(max(df["lcow_high_values"])) + 2,
    )

    fig = plt.gcf()
    fig.tight_layout()
    fig.set_size_inches(7, 5, forward=True)

    plt.show()

    return


if __name__ == "__main__":

    labels = pd.Series({
        'heat_price': "Heat Price ($/kWh)\n 0.00894 [0.00447,0.011175]",
        'cst_cost_per_total_aperture_area':"Cost per Total \nAperture Area (\$/m$^2$)\n 373 [186.5,466.25]",
        'cst_cost_per_storage_capital':"Cost per Thermal \nStorage Capacity ($/kWh)\n 62 [31,77.5]",
        "nacl_recovery_price": "Recovered NaCl Price ($/kg)\n 0 [-0.024,0]",
    })

    # value order corresponds to label order
    lcow_low_values = pd.Series({
        'heat_price': 21.67,
        'cst_cost_per_total_aperture_area': 19.17,
        'cst_cost_per_storage_capital': 18.58,
        "nacl_recovery_price": 17.761187454979,

    } 
    )
    lcow_high_values = pd.Series({
        'heat_price': 22.63,
        'cst_cost_per_total_aperture_area': 23.88,
        'cst_cost_per_storage_capital': 24.18,
        "nacl_recovery_price":22.31,
    } 
    )

    baseline_lcow = 22.31

    df = pd.DataFrame(columns=["labels", "lcow_low_values", "lcow_high_values"])
    df["labels"] = labels
    df["lcow_low_values"] = lcow_low_values
    df["lcow_high_values"] = lcow_high_values

    var_effect = np.abs(lcow_high_values - lcow_low_values) / baseline_lcow

    df["range"] = var_effect

    df = df.sort_values(
        "range", ascending=True, inplace=False, ignore_index=False, key=None
    )

    tornado_plot(baseline_lcow, df, title="ZLD")
