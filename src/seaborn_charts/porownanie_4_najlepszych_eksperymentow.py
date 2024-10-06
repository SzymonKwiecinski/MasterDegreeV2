import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df_2 = pd.read_csv("../experiment_2/report.csv")
df_3 = pd.read_csv("../experiment_3/report.csv")
df = pd.concat([df_3, df_2])

# df = df[df["experiment_name"].isin(["experiment_2b3", "experiment_2b2", "experiment_3b2", "experiment_3b4"])]
experiment_efficiency = df.groupby(["experiment_name", "experiment_iteration"])[
                            "obj_status"].mean() * 100

experiment_cost = df.groupby(["experiment_name", "experiment_iteration"])["sum_price"].mean()

experiment = pd.merge(experiment_efficiency, experiment_cost, on=["experiment_name", "experiment_iteration"])
experiment = experiment.sort_values("sum_price")

# sns.set_theme(rc={'figure.figsize': (20, 20)})
# sns.set_theme(rc={"figure.dpi": 300})

g = sns.jointplot(
    data=experiment,
    x="sum_price", y="obj_status", hue="experiment_name",
    kind="scatter"
)
sns.move_legend(g.ax_joint, "lower right", frameon=False)
plt.grid()
plt.show()

g = sns.displot(experiment, x="obj_status", hue="experiment_name", kind="ecdf")
plt.grid()
plt.show()

"""Tutaj widzimy ze exp 2b2 daje najlesze wyniki"""
sns.catplot(data=experiment, x="experiment_name", y="obj_status", kind="swarm")
plt.show()
