"""
Analiza dla najlepszego eksperymentu dla One Prompt
61 kropek bo jest 61 zadan wykonanych 10 razy
"""


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_2 = pd.read_csv("experiment_2/report.csv")
df_3 = pd.read_csv("experiment_3/report.csv")
df = pd.concat([df_3, df_2])

experiment_name = "experiment_2b2"

experiment_2b3 = df[df["experiment_name"] == experiment_name]

experiment_efficiency = experiment_2b3.groupby(["task_number"])[
                            "obj_status"].mean() * 100

experiment_cost = experiment_2b3.groupby(["task_number"])["sum_price"].mean()

experiment = pd.merge(experiment_efficiency, experiment_cost, on=["task_number"])
experiment = experiment.sort_values("sum_price")

# sns.set_theme(rc={'figure.figsize':(20,20)})
# sns.set_theme(rc={"figure.dpi": 300})

sns.jointplot(x="sum_price", y="obj_status", data=experiment)
plt.grid()
plt.show()

"""Jak rozklada sie wykonalnosc zadan dla tego eksperymentu, ile zadan zostal zrobion 100% razy ile 10% razy"""
sns.histplot(data=experiment, x="obj_status", kde=False, bins=10).set_title(f"Tasks distribution {experiment_name}")
plt.grid()
plt.show()
