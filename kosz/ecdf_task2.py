import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_2 = pd.read_csv("../experiment_2/report.csv")
df_3 = pd.read_csv("../experiment_3/report.csv")
df = pd.concat([df_3, df_2])

df = df[df["experiment_name"].isin(["experiment_2b3", "experiment_2b2", "experiment_3b2", "experiment_3b4"])]
df.head()
df = df[df["task_number"] < 10]
experiment_efficiency = df.groupby(["task_number"])[
                            "obj_status"].mean() * 100  #.sum() / 18 * 100
# task_number
# experiment_efficiency = experiment_efficiency.groupby("experiment_name").mean()

experiment_cost = df.groupby(["task_number"])["sum_price"].mean()
# experiment_cost = experiment_cost.groupby("experiment_name").mean()

experiment = pd.merge(experiment_efficiency, experiment_cost, on=["task_number"])
experiment = experiment.sort_values("sum_price")

sns.set_theme(rc={'figure.figsize':(20,40)})
# sns.set_theme(rc={"figure.dpi": 300})


sns.catplot(data=experiment, x="task_number", y="obj_status", kind="box")
plt.show()

sns.displot(df, x="obj_status", hue="task_number", kind="kde")
plt.show()


# glue = experiment.pivot(index="task_number", columns="obj_status", values="obj_status")
print(experiment)
plt.show()
print(df["obj_status"])