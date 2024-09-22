import pulp
import json

# Given data in JSON format
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

# Model initialization
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("coal", range(1, data['T'] + 1), lowBound=0)
nuke = pulp.LpVariable.dicts("nuke", range(1, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Capacity Constraint
    problem += (
        pulp.lpSum(coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
        data['OilCap'][t - 1] >= data['Demand'][t - 1],
        f"Capacity_Constraint_{t}"
    )
    
    # Nuclear Capacity Constraint
    problem += (
        pulp.lpSum(nuke[j] for j in range(1, t + 1)) <= 
        (data['MaxNuke'] / 100) * pulp.lpSum(coal[j] + nuke[j] + data['OilCap'][t - 1] for j in range(1, t + 1)),
        f"Nuclear_Capacity_Constraint_{t}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')