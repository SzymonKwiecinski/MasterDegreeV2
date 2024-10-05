import pulp

# Data provided
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Extracting data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']
num_products = data['NumProducts']
num_machines = data['NumMachines']

# Initialize the problem
problem = pulp.LpProblem("Product_Production", pulp.LpMaximize)

# Decision variables: Quantities to be produced for each product
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_products)])

# Constraints: Production time on each machine
for s in range(num_machines):
    problem += (pulp.lpSum([produce_time[k][s] * quantity[k] for k in range(num_products)]) <= available_time[s], f"Time_Constraint_Stage_{s}")

# Solve the problem
problem.solve()

# Output the results
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(num_products)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')