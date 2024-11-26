# %% [markdown]
# # Opioid shipping data_plotting

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines

# %%
# Load the data
opd_mme_data_raw = pd.read_csv(
    "/Users/ilseoplee/Desktop/Study/2024 MIDS/Practical Data Science/Final_Opioid_Project/20_intermediate_files/shipping_merged_2007_2015.csv"
)
opd_mme_data_raw.describe()

# %%
# Missing value treatment : drop population below 20K
opd_mme_data = opd_mme_data_raw[opd_mme_data_raw["POPULATION"] > 20000].copy()

# opd_mme_data.head
len(opd_mme_data)

# %%
# MME Multiplier & log transformation
multiplier = 1000000
opd_mme_data["MME_per_capita_multiplier"] = (
    np.log(opd_mme_data["MME_per_capita"] * multiplier) + 1
)
opd_mme_data.head(3)

# %%
# FL filtering
fl_data = opd_mme_data[opd_mme_data["STATE"] == "FL"]

# FL data _ MME per capita multiplier
fl_yearly_summary = fl_data.groupby("YEAR")["MME_per_capita"].mean().reset_index()
fl_yearly_summary_1 = (
    fl_data.groupby("YEAR")["MME_per_capita_multiplier"].mean().reset_index()
)

# check
display(fl_yearly_summary)
display(fl_yearly_summary_1)


# %%
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


# %%
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
        (dataset["STATE"] == testing_state)
        & (dataset["POLICY_IMPLEMENTATION"] == False)
    ]
    post_policy_data = dataset[
        (dataset["STATE"] == testing_state) & (dataset["POLICY_IMPLEMENTATION"] == True)
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
    ax.set_title(f"Pre-Post Analysis for MME_per_1,000,000_people: {testing_state}")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"MME_per_1,000,000_people")

    # Showing the plot
    plt.show()


# %%
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
    plt.title(
        f"Difference-in-Difference Analysis for MME_per_1,000,000_people : {testing_state}"
    )
    plt.xlabel("Year")
    plt.ylabel(f"MME_per_1,000,000_people")

    # Showing plot
    plt.show()


# %%
def all_states_plot(dataset_2, pol_implem_year, metric_column):

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
    plot.set_ylabels(f"MME_per_1,000,000_people", fontsize=12)

    # Displaying the plot with adjusted layout
    plt.tight_layout()
    plt.show()


# %%
# Defining the testing state for the analysis
testing_state = "WA"

# Listing of controlling states for comparison
controlling_states = ["CO", "OR", "MT"]

# Defining key years for the analysis
pol_implem_year = 2012
starting_year = 2008
ending_year = 2015

opd_mme_plot = prepare_data(
    opd_mme_data,
    testing_state,
    controlling_states,
    pol_implem_year,
    starting_year,
    ending_year,
)

opd_mme_plot.head(20)

# %%
# Calling the all_states_plot function to visualize the data
all_states_plot(opd_mme_plot, pol_implem_year, "MME_per_capita_multiplier")

# %%
# Calling the pre_post_plot function to visualize pre-post analysis for mortality: FL
pre_post_plot(opd_mme_plot, testing_state, pol_implem_year, "MME_per_capita_multiplier")

# %%
# Calling the dif_dif_plot function to visualize difference-in-difference analysis for mortality: WA

dif_dif_plot(
    opd_mme_plot,
    testing_state,
    controlling_states,
    pol_implem_year,
    "MME_per_capita_multiplier",
)

# %% [markdown]
# ### Pre-post Analysis and Difference-in-Difference Analysis for Florida

# %%
# Defining the testing state for the analysis
testing_state = "FL"

# Listing of controlling states for comparison
controlling_states = ["GA", "NC", "SC"]

# Defining key years for the analysis
pol_implem_year = 2010
starting_year = 2006
ending_year = 2013

mme_opd_plot = prepare_data(
    opd_mme_data,
    testing_state,
    controlling_states,
    pol_implem_year,
    starting_year,
    ending_year,
)

mme_opd_plot

# %%
# Calling the all_states_plot function to visualize the data
all_states_plot(mme_opd_plot, pol_implem_year, "MME_per_capita_multiplier")

# %%
# Calling the pre_post_plot function to visualize pre-post analysis for mortality: FL
pre_post_plot(mme_opd_plot, testing_state, pol_implem_year, "MME_per_capita_multiplier")

# %%
# Calling the dif_dif_plot function to visualize difference-in-difference analysis for mortality: FL
dif_dif_plot(
    mme_opd_plot,
    testing_state,
    controlling_states,
    pol_implem_year,
    "MME_per_capita_multiplier",
)
