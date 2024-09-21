import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Extract data
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables: Quantity of each product to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective function: Maximize total profit
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumProducts)]), "Total_Profit"

# Constraints

# Production time constraints for each machine
for m in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][m] * x[k] for k in range(NumProducts)]) <= AvailableTime[m], f"Machine_{m}_Time"

# Solve the problem
problem.solve()

# Print the results
for k in range(NumProducts):
    print(f'Product {k + 1} production quantity: {pulp.value(x[k])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')