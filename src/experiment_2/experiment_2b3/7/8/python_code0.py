import pulp

# Data from the input format
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Number of parts and machines
K = data['NumParts']
S = data['NumMachines']

# Time taken for each part in each machine
time = data['Time']

# Profit from each part
profit = data['Profit']

# Capacity of each machine
capacity = data['Capacity']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each part to be produced
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(K)]), "TotalProfit"

# Constraints: Respect the capacity of each machine
for s in range(S):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(K)]) <= capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Output the quantities in the required format
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')