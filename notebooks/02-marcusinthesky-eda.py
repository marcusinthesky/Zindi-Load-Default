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

# %% [markdown]
# Make use of an isolation forest to get a score of ruralness based on existing custoemr GPS coordinates.

# %%
from sklearn.ensemble import IsolationForest

badness = traindemographics.merge(trainperf, on="customerid", how="inner").assign(
    age=lambda df: (pd.to_datetime("today") - df.birthdate) / pd.np.timedelta64(1, "Y")
)
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
X = badness.assign(isolation_score=isolation_score).loc[
    :, ["isolation_score", "age", "loanamount", "termdays"]
]


# %% [markdown]
# Looked to explore custer analysis on the data, using 'isolation_score', 'age','loanamount', 'termdays'.

# %%
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

# %% [markdown]
# Looked to analyze the Pricinple Compoents in this data to detemine segments.

# %%
pipeline = Pipeline([("scale", StandardScaler()), ("pca", PCA())])

# %%
Z = pipeline.fit_transform(X)
pd.DataFrame(Z[:, :2], columns=["Component 1", "Component 2"]).hvplot.scatter(
    "Component 1", "Component 2"
)

# %%
pd.Series(pipeline.named_steps["pca"].explained_variance_ratio_).hvplot.bar(
    title="Explained Variance"
)

# %%
X.hvplot.scatter("isolation_score", "age")

# %%
from scipy.stats import pearsonr

# %%
pearsonr(X.isolation_score, X.age)

# %%
from sklearn.linear_model import LogisticRegression

# %%
lm = LogisticRegression()

# %%
lm.fit(X, badness.good_bad_flag == "Bad")

# %%
lm.coef_

# %%
import statsmodels.api as sm

# %%
log_reg = sm.Logit(badness.good_bad_flag == "Bad", X.assign(bias=1)).fit()

# %%
log_reg.summary()

# %%
s
