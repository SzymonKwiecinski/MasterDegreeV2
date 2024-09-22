import pulp

# Parse the data
data = {
    'NumProducts': 2, 
    'NumMachines': 2, 
    'ProduceTime': [[1, 3], [2, 1]], 
    'AvailableTime': [200, 100], 
    'Profit': [20, 10]
}

num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function
problem += pulp.lpSum([quantities[k] * profit[k] for k in range(num_products)])

# Constraints
for s in range(num_machines):
    problem += pulp.lpSum([quantities[k] * produce_time[k][s] for k in range(num_products)]) <= available_time[s]

# Solve the problem
problem.solve()

# Collect the results
results = {
    "quantity": [pulp.value(quantities[k]) for k in range(num_products)]
}

# Output the results
print(results)

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')