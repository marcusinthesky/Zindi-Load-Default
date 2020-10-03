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
traindemographics = context.catalog.load("traindemographics")
testdemographics = context.catalog.load("testdemographics")
trainperf = context.catalog.load("trainperf")
testperf = context.catalog.load("testperf")
trainprevloans = context.catalog.load("trainprevloans")
testprevloans = context.catalog.load("testprevloans")

# %%
traindemographics.describe()

# %%
testdemographics.describe()

# %%
