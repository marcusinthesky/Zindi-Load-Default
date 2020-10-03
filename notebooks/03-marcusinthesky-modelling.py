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
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.metrics import f1_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer, make_column_selector
from catboost import CatBoostClassifier
import holoviews as hv
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

# %%
trainperf

# %%
traindemographics

# %%
trainprevloans

# %% [markdown]
# # Baseline Model

# %%
X_train, y_train = (
    trainperf.drop(columns=["good_bad_flag"]).select_dtypes(include="number"),
    trainperf.loc[:, "good_bad_flag"],
)
X_test = testperf.select_dtypes(include="number")

pd.testing.assert_series_equal(
    X_test.dtypes, X_train.dtypes
)  # here we validate that our types are the same across our submission results
pd.testing.assert_index_equal(
    X_test.columns, X_train.columns
)  # here we validate that our names are equal

# %%
model = CatBoostClassifier(iterations=100, verbose=0)

# %%
param_distributions = {"model__iterations": [100, 101]}

# %%
pipeline = Pipeline([("model", model)])

# %%
cv = TimeSeriesSplit(3)

# %%
pipeline.get_params()

# %%
search = RandomizedSearchCV(
    pipeline,
    cv=cv,
    param_distributions=param_distributions,
    scoring="accuracy",
    return_train_score=True,
)

# %%
search.fit(X_train, y_train)

# %%
pd.DataFrame(search.cv_results_)

# %%
y_pred = search.predict(X_test)
submission = samplesubmission.assign(Good_Bad_flag=y_pred)
submission

# %%
context.catalog.save("submission", submission)
