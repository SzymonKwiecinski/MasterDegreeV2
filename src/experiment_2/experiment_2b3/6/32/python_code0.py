import pulp

# Extract data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective function
problem += pulp.lpSum([Profit[k] * quantity[k] for k in range(NumProducts)])

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][s] * quantity[k] for k in range(NumProducts)]) <= AvailableTime[s]

# Solve the problem
problem.solve()

# Output the results
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(NumProducts)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')