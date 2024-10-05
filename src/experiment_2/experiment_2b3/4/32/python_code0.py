import pulp

# Parsing input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for quantities of each product
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_products))

# Constraints: Production time constraints for each machine
for s in range(num_machines):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(num_products)) <= available_time[s]

# Solve the problem
problem.solve()

# Output format
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(num_products)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')