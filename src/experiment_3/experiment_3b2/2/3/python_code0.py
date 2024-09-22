import pulp
import json

# Data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0)
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

# Capacity constraints
for t in range(1, data['T'] + 1):
    problem += (
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
        data['OilCap'][t - 1] >= data['Demand'][t - 1]
    )

# Nuclear capacity constraints
for t in range(1, data['T'] + 1):
    problem += (
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) <=
        (data['MaxNuke'] / 100) * (
            pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
            pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
            data['OilCap'][t - 1]
        )
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')