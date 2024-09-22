import pulp

# Data from the problem
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Unpack data
num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantities = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function
problem += pulp.lpSum(profit[k] * quantities[k] for k in range(num_products)), "Total_Profit"

# Constraints for each machine
for s in range(num_machines):
    problem += (pulp.lpSum(produce_time[k][s] * quantities[k] for k in range(num_products)) <= available_time[s]), f"Time_Constraint_Stage_{s}"

# Solve the problem
problem.solve()

# Retrieve results
output = {"quantity": [pulp.value(quantities[k]) for k in range(num_products)]}

# Print results and objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')