import pulp
import json

# Input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extract data
K = data['NumProducts']  # Number of products
S = data['NumMachines']  # Number of stages
produce_time = data['ProduceTime']  # Produce time for each product at each stage
available_time = data['AvailableTime']  # Available time for each stage
profit = data['Profit']  # Profit for each product

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s]), f"Constraint_stage_{s}"

# Solve the problem
problem.solve()

# Output the production quantities
output_quantity = [pulp.value(quantity[k]) for k in range(K)]

# Display results
results = {"quantity": output_quantity}
print(json.dumps(results))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')