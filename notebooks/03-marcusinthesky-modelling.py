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
import shap

shap.initjs()
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
# # Baseline Model

# %% [markdown]
# We will create our baseline test and training model and validate that these datasets are of the same name and types. This will use only a small handful of features which allows us to limit he amount of feature engineering and data engienering we would require, and which would be time consuming.

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

# %% [markdown]
# One thing which may be of concern to our model and scoring metric may be class imbalance, we may want to correct for this using SMOTE or random oversampling using packages like `Imbalance-learn`.

# %%
y_train.value_counts()

# %% [markdown]
# We will be choosing as baseline, as CatBoost model. Histgram gradient boosting models have tremendous robustness to overfitting and provide explainabilitu advantages.

# %%
model = CatBoostClassifier(iterations=100, verbose=0)

# %% [markdown]
# As a baseline we will be leaning on `RandomizedSearchCV` to do our cross validation, so will just start with a mostly meaningless gridsearch to collect our satistics on model train and test performance.

# %%
param_distributions = {"model__iterations": [100, 101]}

# %%
pipeline = Pipeline([("model", model)])

# %% [markdown]
# We will rely on a time-series backtesting type splite. We noticed our data is segmented on time between test and train and this would then provide the greatest analoge to real-world testing over a random shuffle.

# %%
cv = TimeSeriesSplit(3)

# %%
pipeline.get_params()

# %% [markdown]
# While we would like to rely on Bayesian Hyperparameter Optimization we would, for now, like to use Randomized Search due to its clear advantages over grid search in setting computational budgets and in performance.

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

# %% [markdown]
# We are going to version our model to keep track of changes and provide later auditing.

# %%
context.catalog.save("baseline_model", search)

# %% [markdown]
# We will save our model to an MLFLow model for simple model serving on Azure, Databricks or Sagemaker.

# %%
mlflow.sklearn.save_model(
    search,
    path=context.project_path / "mlruns" / "1",
    conda_env=context.project_path / "src" / "conda_env.yml",
)

# %%
mlflow.sklearn.get_default_conda_env()

# %% [markdown]
# We will look at the result of our baseline model.

# %%
pd.DataFrame(search.cv_results_)

# %% [markdown]
# We will begin analyzing our model by investigating the feature importances across the model.

# %%
pd.Series(tree.feature_importances_, index=X_train.columns).hvplot.bar(
    title="Feature Importances"
)

# %% [markdown]
# We will use SHAP to provide some insights into model explainability in order to understand interaction in our model and possible signs of algorithmic bias or issuesin fairnesss.

# %%
tree = search.best_estimator_.named_steps["model"]

# %%
X_sample = X_train.sample(n=1000)

# %%
explainer = shap.TreeExplainer(tree, model_output="probability", data=X_sample)

# %%
shap_values = explainer.shap_values(X_sample)

# %% [markdown]
# Looking our local explainations, we see the important impact of interaction in our model. With loan number important at some of our extremes.

# %%
shap.force_plot(explainer.expected_value, shap_values, X_sample)

# %% [markdown]
# We will perform inference and do an example submission.

# %%
y_pred = search.predict(X_test)
submission = samplesubmission.assign(Good_Bad_flag=y_pred)
submission

# %%
context.catalog.save("submission", submission)
