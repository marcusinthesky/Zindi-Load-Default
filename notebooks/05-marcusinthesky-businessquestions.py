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
# __1. What would be your recommendation to the client based on your analysis?__
# This is a growth business. With many customers fist time users of the platform.

# %% [markdown]
# ![](past.png)

# %% [markdown]
# Given this growth having stable predictive models may be difficult, as you don't see the important long-term and seasonal trends which often charcterize distress. I would focus heavily on understanding your customer, segmenting particular groups and developing high impact, data-driven campaigns to grow your business. Lookiing at your referal system, this may be such a campaign and is one we would recommend continued investment in. Clearly your loans attract customers of all ages, and unsurprisingly older customers tend to repay more consistently. This may require you to reposition your brand to families, rather than young persons if you are looking to target in your growth high quality loans.

# %% [markdown]
# ![](age.png)s

# %% [markdown]
# We did some work on the geographic layout of your customers. There appear to be some outliers in the US, China and Europe. This may be a data integrity issue to be interrogates.

# %% [markdown]
# ![](map.png)

# %% [markdown]
# To segment your customers, we look to common dimensionality reduction and clustering techniques, but found that age and geographic isolation appeared valuable correlated features on which to segment custoemrs, which were positively correlated and highly statistically significant (0.04746782058599189, 0.006571857864108819).

# %% [markdown]
# ![](isolation_age.png)

# %% [markdown]
# __2. Please provide 1 relevant & interesting visualization and describe it to your client?__

# %% [markdown]
# Comparing age and isolation, we see again seperability between isolation debtors. This suggests that more central customers in urban areas tend to have better debt.

# %% [markdown]
# ![](isolation.png)

# %% [markdown]
# This is supported by Logistic Regression Analysis, which shows controlling for term and amount; older, urban customers tend to have lower default rates.

# %% [markdown]
# ![](logistic.png)

# %% [markdown]
# Beyond, predicting default, these provide actionable insights to attract new customers and grow your business.

# %% [markdown]
# __3. If you were allows to use external data what kind of data would you think of?__
# I would really like population statistics from Nigeria to compare agianst country ages and population density in particular regions. There may be regions with very similar demographics which may be a great place fro them to target.

# %% [markdown]
# __4. What would have been your next step if you had more time?__
# I managed to construct a working data pipeline, RESTAPI and data versioning. Which I thought quite productive. I would have liked to have had more time of predictive model development and feature engineering, but I thought given the size of the data, its censorship and quality, it would be better for this customer to focus on segmentation and growth, rather than a predictive model fit to only a few days worth of days. I wanted to do more more on algorithmic fairness using IBM AIF360 and class imbalance using Imblearn, but just didnt have the time.

# %% [markdown]
# __5. Do you have any comments/feedback about the assesment?__
# I have raised this on Zindi message boards many times, I love their branch, but there competitions are poorly specified. In default prediction, you have to take into account the fact that some debt is close to default but just hasn't defaulted yet. When you have any section of data though time you are going to have censorship, where certain loans havent come to term but may be highly likely to default. You take this into account using survival analysis, which provides you a log hazard of default. Using accuracy as a score is a poor metric, even in classification problems, which this should not be. \\
# \\
# That being said I loved the mix of strategic and ML questions.
