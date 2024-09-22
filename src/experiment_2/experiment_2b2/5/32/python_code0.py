import pulp

# Read the data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Number of products and machines
num_products = data['NumProducts']
num_machines = data['NumMachines']

# Extract the required data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: quantity to produce for each product
quantity_vars = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity_vars[k] for k in range(num_products)), "Total_Profit"

# Constraints: Production time constraints for each machine
for s in range(num_machines):
    problem += (pulp.lpSum(produce_time[k][s] * quantity_vars[k] for k in range(num_products)) <= available_time[s]), f'Constraint_Machine_{s}'

# Solve the problem
problem.solve()

# Output the quantities to be produced
quantity = [pulp.value(quantity_vars[k]) for k in range(num_products)]
result = {"quantity": quantity}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')