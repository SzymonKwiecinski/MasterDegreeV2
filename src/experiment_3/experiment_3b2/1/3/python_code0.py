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
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Demand Satisfaction
    demand_constraint = (
        data['OilCap'][t - 1] +
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    )
    problem += demand_constraint >= data['Demand'][t - 1]

    # Nuclear Capacity Limit
    max_nuke_constraint = pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    total_capacity = (
        data['OilCap'][t - 1] +
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    )
    problem += max_nuke_constraint <= (data['MaxNuke'] / 100) * total_capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')