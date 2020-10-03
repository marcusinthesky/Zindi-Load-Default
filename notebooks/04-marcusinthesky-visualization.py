# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: zindi_load_default
#     language: python
#     name: python3
# ---

# %%
import holoviews as hv
import pandas as pd
import hvplot.pandas  # noqa

hv.extension("bokeh")

# %%
traindemographics = context.catalog.load("traindemographics")
testdemographics = context.catalog.load("testdemographics")
trainperf = context.catalog.load("trainperf")
testperf = context.catalog.load("testperf")
trainprevloans = context.catalog.load("trainprevloans")
testprevloans = context.catalog.load("testprevloans")
samplesubmission = context.catalog.load("SampleSubmission")

# %% [markdown]
# There seems no obvious indication that load in Europe, China or the USA have higher probabilities of default, but appears odd that these have not been screened as it may be far harder to collect these debt when they go bad. This may also signal a data integrity issue.

# %%
badness = traindemographics.merge(trainperf, on="customerid", how="inner").assign(
    age=lambda df: (pd.to_datetime("today") - df.birthdate) / pd.np.timedelta64(1, "Y")
)


badness.hvplot.points(
    "longitude_gps",
    "latitude_gps",
    geo=True,
    color="good_bad_flag",
    alpha=0.5,
    xlim=(-118.247009, 151.209290),
    ylim=(-33.868818, 71.228069),
    tiles=True,
    width=1200,
    heigth=800,
    title="Location of Loans",
)

# %% [markdown]
# We do tend to see good debt in regions densely occupied by existing customers. This may suggest a strategy which targets customers in urban areas, across netowrks of friends and family.

# %%
from sklearn.ensemble import IsolationForest

isolatio_forest = IsolationForest()
isolatio_forest.fit(
    traindemographics.loc[
        :,
        [
            "longitude_gps",
            "latitude_gps",
        ],
    ]
)
isolation_score = isolatio_forest.decision_function(
    badness.loc[
        :,
        [
            "longitude_gps",
            "latitude_gps",
        ],
    ]
)
badness.assign(isolation_score=isolation_score).hvplot.kde(
    "isolation_score",
    by="good_bad_flag",
    title="Geographic Isolation Scores",
    width=1200,
    height=400,
)

# %%
trainperf.hvplot.kde(
    "loanamount",
    by="good_bad_flag",
    title="Distribution of Good and Bad Loans on Loan Amount",
)

# %% [markdown]
# There is no evidence that it takes longer to approve uncertain loans.

# %%
trainperf.assign(
    days_to_approve=lambda df: (df.approveddate - df.creationdate).dt.total_seconds()
    // (60 ** 2)
).groupby("good_bad_flag").days_to_approve.median().hvplot.bar(title="Hours to Approve")

# %% [markdown]
# Given such a small sample, there is no evidence that the day of week of approoval affects default probability, though we imagine given a larger sample day of month may.

# %%
trainperf.assign(bad_debt=pd.get_dummies(trainperf.good_bad_flag).Bad).assign(
    day_of_week=lambda df: df.creationdate.dt.day_name()
).groupby("day_of_week").bad_debt.mean().hvplot.bar(
    title="Default Probability per Day Created"
)

# %% [markdown]
# Looking to the data, provided most customers are first-time users, with only a small fraction regular users of the platform.

# %%
trainprevloans.groupby(
    "customerid", observed=True
).loannumber.count().value_counts().hvplot.bar(
    title="Number of customers with number of past loans"
)

# %% [markdown]
# Savings accounts are dominant in the sample.

# %%
traindemographics.bank_account_type.value_counts().hvplot.bar()

# %% [markdown]
# Understandably good customers tend to be a bit older customers.

# %%
badness.hvplot.kde(
    "age", by="good_bad_flag", title="Distribution of Good and Bad Loans on Loan Amount"
)

# %% [markdown]
# Ideally we would want to analysis this data using survival analysis to take into issues of censorship, ordinary modelling techniques cannot account for.

# %%
from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter()

# %%
debts = (
    trainprevloans.assign(
        debt_age=lambda df: (df.closeddate - df.approveddate).dt.days.clip(0, 40)
    )
    .assign(good_bad_flag="Good")
    .assign(paid=lambda df: df.good_bad_flag.ne("Good").astype(int))
    .pipe(
        lambda df: pd.concat(
            [
                df,
                trainperf.assign(
                    debt_age=lambda df: (
                        df.approveddate.max() - df.approveddate
                    ).dt.days
                ).assign(
                    paid=lambda df: -df.good_bad_flag.replace({"Good": -1, "Bad": 1})
                ),
            ]
        )
    )
)
debts

# %%
(debts.debt_age - debts.termdays).clip(0, pd.np.inf).replace(0, pd.np.nan).hvplot.kde(
    title="Distributionof Overdue Debt"
)

# %%
kmf.fit(debts.debt_age, event_observed=debts.paid.replace(-1, 0))
kmf.survival_function_.hvplot.line(title="Survival function of political regimes")
