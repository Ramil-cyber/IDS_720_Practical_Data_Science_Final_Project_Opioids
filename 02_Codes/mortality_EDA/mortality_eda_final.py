# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines

# Reading the mortality dataset
pd.set_option("display.max_columns", None)

mortality_data = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/03_Results/mortality_population.csv?token=GHSAT0AAAAAACZHZQITZSCVIT7OLYF6BBKAZ2CPIDA"
)
mortality_data

# Createing 'MORTALITY_DATA' column
mortality_data["MORTALITY_DATA"] = (
    mortality_data["DEATHS"] / mortality_data["POPULATION"]
)
mortality_data

# Defining normalization factor in order to normalize 'Mortality_Rate' column
norm_mort_mult = 1000000

# Createing 'Norm_mort_mult' column in the dataframe by multiplying 'Mortality_Rate' by normalization factor
mortality_data["MORM_MORT_MULT"] = mortality_data["MORTALITY_DATA"] * norm_mort_mult

# Seting the label for the y-axis, formatted with the normalization factor
ylabels = f"Mortality per 1 mln people"
ylabels

mortality_data

def prepare_data(
    dataset,
    testing_state,
    controlling_states,
    pol_impl_year,
    starting_year,
    ending_year,
):
    """
    Parameters:
        dataset (DataFrame): The original dataset to be processed.
        testing_state (str): The state where the policy is implemented (Test state).
        controlling_states (list): List of control states for comparison.
        pol_impl_year (int): The year the policy was implemented.
        starting_year (int): The first year of the analysis period.
        ending_year (int): The last year of the analysis period.
    """

    # Combining test and control states to filter
    relevant_states = [testing_state] + controlling_states

    # Filtering the dataset based on the relevant states and years
    filtered_dataset = dataset[
        (dataset["STATE"].isin(relevant_states))
        & (dataset["YEAR"].between(starting_year, ending_year))
    ].copy()

    # Adding column indicating whether the policy is pre or post implementation
    filtered_dataset["POLICY_IMPLEMENTATION"] = (
        filtered_dataset["YEAR"] >= pol_impl_year
    )

    # Labelling each state as 'Test' or 'Control' based on the provided states
    filtered_dataset["STATE_TYPE"] = filtered_dataset["STATE"].apply(
        lambda state: "Test" if state == testing_state else "Control"
    )

    return filtered_dataset

def pre_post_plot(dataset_2, testing_state, pol_implem_year, metric_column):
    """
    Parameters:
        dataset_2 (DataFrame): The dataset to be visualized.
        metric_column (str): The column representing the metric to plot ("MORM_MORT_MULT").
    """

    # Creating a copy of the dataset to avoid modifying the original DataFrame
    dataset = dataset_2.copy()

    # Seting up the plot
    fig, ax = plt.subplots(figsize=(8, 4))

    # Defining the data for pre-policy and post-policy analysis
    pre_policy_data = dataset[
        (dataset["STATE"] == testing_state) & (dataset["POLICY_IMPLEMENTATION"] == True)
    ]
    post_policy_data = dataset[
        (dataset["STATE"] == testing_state)
        & (dataset["POLICY_IMPLEMENTATION"] == False)
    ]

    # Ploting pre-policy trend line
    sns.regplot(
        data=pre_policy_data,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "red"},
        ax=ax,
        scatter=False,
    )

    # Ploting post-policy trend line
    sns.regplot(
        data=post_policy_data,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "blue"},
        ax=ax,
        scatter=False,
    )

    # Adding a vertical line at the policy implemented year
    ax.axvline(pol_implem_year, ls="--", color="black", label="Policy Implemented Year")

    # Defining the legend
    legend_handles = [
        mlines.Line2D([], [], color="red", label="Post-Policy"),
        mlines.Line2D([], [], color="blue", label="Pre-Policy"),
        mlines.Line2D(
            [], [], color="black", label="Policy Implemented Year", linestyle="--"
        ),
    ]
    ax.legend(handles=legend_handles, loc="lower right")

    # Adding titles and labels
    ax.set_title(f"Pre-Post Analysis for Mortality: {testing_state}")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Mortality per 1 mln people")

    # Showing the plot
    plt.show()

def dif_dif_plot(
    dataset_2, testing_state, controlling_state, pol_implem_year, metric_column
):

    # Creating a copy of the dataset to avoid modifying the original DataFrame
    dataset = dataset_2.copy()

    # Seting up the plot
    fig, ax = plt.subplots(figsize=(8.2, 4))

    # Filtering data for pre- and post-policy periods
    test_state_pre = dataset[
        (dataset["STATE"] == testing_state)
        & (dataset["POLICY_IMPLEMENTATION"] == False)
    ]
    test_state_post = dataset[
        (dataset["STATE"] == testing_state) & (dataset["POLICY_IMPLEMENTATION"] == True)
    ]
    control_states_pre = dataset[
        (dataset["STATE"].isin(controlling_state))
        & (dataset["POLICY_IMPLEMENTATION"] == False)
    ]
    control_states_post = dataset[
        (dataset["STATE"].isin(controlling_state))
        & (dataset["POLICY_IMPLEMENTATION"] == True)
    ]

    # Ploting difference-in-difference analysis for testing and controlling states
    sns.regplot(
        data=test_state_pre,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "blue"},
        ax=ax,
        scatter=False,
    )
    sns.regplot(
        data=test_state_post,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "blue"},
        ax=ax,
        scatter=False,
    )
    sns.regplot(
        data=control_states_pre,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "red"},
        ax=ax,
        scatter=False,
    )
    sns.regplot(
        data=control_states_post,
        x="YEAR",
        y=metric_column,
        line_kws={"color": "red"},
        ax=ax,
        scatter=False,
    )

    # Adding a vertical line for the policy implementation year
    ax.axvline(pol_implem_year, ls="--", color="black", label="Policy Implemented Year")

    # Adding legend
    plt.legend(
        handles=[
            mlines.Line2D([], [], color="blue", label="Test State (Pre/Post)"),
            mlines.Line2D([], [], color="red", label="Control States (Pre/Post)"),
            mlines.Line2D([], [], color="black", linestyle="--", label="Policy Year"),
        ],
        loc="lower right",
    )

    # Seting titles and labels
    plt.title(f"Difference-in-Difference Analysis for Mortality: {testing_state}")
    plt.xlabel("Year")
    plt.ylabel(f"Mortality per 1 mln people")

    # Showing plot
    plt.show()

def all_states_plot(dataset_2, pol_implem_year, metric_column, norm_mort_mult=1000000):

    # Creating a copy of the dataset to avoid modifying the original DataFrame
    dataset = dataset_2.copy()

    # Creating the lmplot for the dataset with state-wise breakdown
    plot = sns.lmplot(
        data=dataset,
        x="YEAR",
        y=metric_column,
        hue="POLICY_IMPLEMENTATION",
        legend=False,
        row="STATE",
        height=4,
        aspect=1.75,
    )

    # Seting titles for each subplot using the state names
    plot.set_titles("{row_name}", fontsize=12)

    # Adding a vertical line at the policy implementation year
    for ax in plot.axes.flat:
        ax.axvline(
            pol_implem_year,
            ls="--",
            color="black",
            lw=2,
            label="Policy Implementated Year",
        )

    plt.legend(
        loc="lower right",
        ncol=2,
    )

    ax = plot.axes[0, 0]

    # Adjusting labels and add a legend
    plot.set_axis_labels("Year", metric_column, fontsize=12)
    plot.set_ylabels(f"Mortality per 1 mln people", fontsize=12)

    # Displaying the plot with adjusted layout
    plt.tight_layout()
    plt.show()

    # Defining the testing state for the analysis
testing_state = "WA"

# Listing of controlling states for comparison
controlling_states = ["CO", "OR", "MT"]

# Defining key years for the analysis
pol_implem_year = 2012
starting_year = 2008
ending_year = 2015

mortality_plot = prepare_data(
    mortality_data,
    testing_state,
    controlling_states,
    pol_implem_year,
    starting_year,
    ending_year,
)

mortality_plot

# Calling the all_states_plot function to visualize the data
all_states_plot(mortality_plot, pol_implem_year, "MORM_MORT_MULT")

# Calling the pre_post_plot function to visualize pre-post analysis for mortality: WA
pre_post_plot(mortality_plot, testing_state, pol_implem_year, "MORM_MORT_MULT")

# Calling the dif_dif_plot function to visualize difference-in-difference analysis for mortality: WA

dif_dif_plot(
    mortality_plot, testing_state, controlling_states, pol_implem_year, "MORM_MORT_MULT"
)

# Defining the testing state for the analysis
testing_state = "FL"

# Listing of controlling states for comparison
controlling_states = ["GA", "NC", "SC"]

# Defining key years for the analysis
pol_implem_year = 2010
starting_year = 2006
ending_year = 2013

mortality_plot = prepare_data(
    mortality_data,
    testing_state,
    controlling_states,
    pol_implem_year,
    starting_year,
    ending_year,
)

mortality_plot

# Calling the all_states_plot function to visualize the data
all_states_plot(mortality_plot, pol_implem_year, "MORM_MORT_MULT")

# Calling the pre_post_plot function to visualize pre-post analysis for mortality: FL
pre_post_plot(mortality_plot, testing_state, pol_implem_year, "MORM_MORT_MULT")

# Calling the dif_dif_plot function to visualize difference-in-difference analysis for mortality: FL
dif_dif_plot(
    mortality_plot, testing_state, controlling_states, pol_implem_year, "MORM_MORT_MULT"
)

