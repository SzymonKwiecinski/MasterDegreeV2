import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(num_products)]

# Objective Function
problem += pulp.lpSum([profit[k] * x[k] for k in range(num_products)]), "Total Profit"

# Constraints
for m in range(num_machines):
    problem += pulp.lpSum([produce_time[k][m] * x[k] for k in range(num_products)]) <= available_time[m], f"Machine_{m}_Time"

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')