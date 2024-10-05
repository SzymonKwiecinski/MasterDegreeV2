import pulp
import json

# Data from the provided JSON format
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Unload", range(1, data['T'] + 1), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("Storage", range(0, data['T'] + 1), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Cranes", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(1, data['T'] + 1))

# Constraints
# (1) Load containers to satisfy demand
for t in range(1, data['T'] + 1):
    if t == 1:
        problem += x[t] + data['InitContainer'] == data['Demands'][t-1] + s[t]
    else:
        problem += x[t] + s[t-1] == data['Demands'][t-1] + s[t]

# (2) Final yard condition
problem += s[data['T']] == 0

# (3) Unloading capacity constraint
for t in range(1, data['T'] + 1):
    problem += x[t] <= data['UnloadCapacity'][t-1]

# (4) Maximum yard capacity constraint
for t in range(1, data['T'] + 1):
    problem += s[t] <= data['MaxContainer']

# (5) Crane capacity constraint
for t in range(1, data['T'] + 1):
    problem += data['Demands'][t-1] <= data['CraneCapacity'] * y[t]

# (6) Maximum number of cranes constraint
for t in range(1, data['T'] + 1):
    problem += y[t] <= data['NumCranes']

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')