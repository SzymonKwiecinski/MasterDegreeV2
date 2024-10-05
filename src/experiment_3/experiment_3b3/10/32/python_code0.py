import pulp

# Extract data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

num_products = data['NumProducts']
num_stages = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_products)), "Total_Profit"

# Constraints for production time in each stage
for s in range(num_stages):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(num_products)) <= available_time[s], f"Stage_{s}_Time"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')