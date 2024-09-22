import pulp
import json

data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extract data from JSON
K = data['NumProducts']  # Number of products
S = data['NumMachines']  # Number of machines
produce_time = data['ProduceTime']  # Produce time for each product for each machine
available_time = data['AvailableTime']  # Available time for each machine
profit = data['Profit']  # Profit for each product

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s], f"Machine_{s+1}_Time"

# Solve the problem
problem.solve()

# Prepare the output
result = {"quantity": [pulp.value(quantity[k]) for k in range(K)]}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')