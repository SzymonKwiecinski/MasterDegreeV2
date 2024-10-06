import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_2 = pd.read_csv("../experiment_2/report.csv")
df_3 = pd.read_csv("../experiment_3/report.csv")
df = pd.concat([df_3, df_2])

df = df[df["experiment_name"].isin(["experiment_2b3", "experiment_2b2", "experiment_3b2", "experiment_3b4"])]
df.head()
experiment_efficiency = df.groupby(["experiment_name", "task_number"])[
                            "obj_status"].mean() * 100  #.sum() / 18 * 100
# task_number
# experiment_efficiency = experiment_efficiency.groupby("experiment_name").mean()

experiment_cost = df.groupby(["experiment_name", "task_number"])["sum_price"].mean()
# experiment_cost = experiment_cost.groupby("experiment_name").mean()

experiment = pd.merge(experiment_efficiency, experiment_cost, on=["experiment_name", "task_number"])
experiment = experiment.sort_values("sum_price")

sns.set_theme(rc={'figure.figsize':(20,20)})
sns.set_theme(rc={"figure.dpi": 300})



sns.catplot(data=experiment, x="experiment_name", y="obj_status", kind="swarm")
plt.show()

sns.catplot(data=experiment, x="experiment_name", y="obj_status", kind="violin")
plt.show()
