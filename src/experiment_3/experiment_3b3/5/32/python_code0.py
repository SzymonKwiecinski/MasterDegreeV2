import pulp

# Problem data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Production time and profit data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Constraints for each machine stage
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]

# Solve the problem
problem.solve()

# Output the results
quantities = [pulp.value(x[k]) for k in range(K)]
print(f'Product Quantities: {quantities}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')