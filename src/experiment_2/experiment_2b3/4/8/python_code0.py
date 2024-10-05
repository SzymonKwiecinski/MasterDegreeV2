import pulp

# Data from the JSON input
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

NumParts = data['NumParts']
NumMachines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(NumParts)]

# Define objective function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(NumParts)])

# Define constraints
for s in range(NumMachines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(NumParts)]) <= capacity[s]

# Solve the problem
problem.solve()

# Prepare the output in the required JSON format
output = {"quantity": [int(pulp.value(quantity[k])) for k in range(NumParts)]}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')