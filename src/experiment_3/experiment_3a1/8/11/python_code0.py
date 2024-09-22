import pulp

# Data from the provided JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Define the problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(1, data['T'] + 1), lowBound=0)  # units produced
I = pulp.LpVariable.dicts("I", range(1, data['T'] + 1), lowBound=0)  # inventory

# Objective function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
           pulp.lpSum(data['SwitchCost'] * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, data['T']))  # for switching costs

# Constraints
# Inventory at the end of the first month
problem += I[1] == x[1] - data['Deliver'][0]

# Inventory for subsequent months
for i in range(2, data['T'] + 1):
    problem += I[i] == I[i - 1] + x[i] - data['Deliver'][i - 1]

# Inventory should be non-negative
for i in range(1, data['T'] + 1):
    problem += I[i] >= 0

# Production should be non-negative
for i in range(1, data['T'] + 1):
    problem += x[i] >= 0
    
# Last month production constraint
problem += x[data['T'] + 1] == 0  # No production after month T

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')