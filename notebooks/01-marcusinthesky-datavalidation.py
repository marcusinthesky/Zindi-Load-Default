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

# %% [markdown]
# We are going to analyze each of our datasets to ensure they are correctly types and update our data catalog to ensure they conform correctly. We are going to try our best to ensure all our data types are stores in the most efficient manner possible to better manage memory, this will involve ensuring the data is stored as pd.Categorical rather than strong types.

# %% [markdown]
# # traindemographics

# %%
traindemographics = context.catalog.load("traindemographics")
traindemographics

# %%
traindemographics.dtypes

# %% [markdown]
# # testdemographics

# %%
testdemographics = context.catalog.load("testdemographics")
testdemographics

# %%
testdemographics.dtypes

# %% [markdown]
# # trainperf

# %%
trainperf = context.catalog.load("trainperf")
trainperf

# %%
trainperf.dtypes

# %% [markdown]
# # testperf

# %%
testperf = context.catalog.load("testperf")
testperf

# %%
testperf.dtypes

# %% [markdown]
# # trainprevloans

# %%
trainprevloans = context.catalog.load("trainprevloans")
trainprevloans

# %%
trainprevloans.dtypes

# %% [markdown]
# # testprevloans

# %%
ctestprevloans

# %%
testprevloans.dtypes

# %% [markdown]
# # sample submission

# %%
samplesubmission = context.catalog.load("SampleSubmission")
samplesubmission


# %%
samplesubmission.dtypes
