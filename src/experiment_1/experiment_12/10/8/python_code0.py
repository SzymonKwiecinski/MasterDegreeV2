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
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Define the Linear Programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumProducts)]), "Total Profit"

# Constraints
# Production time constraints for each machine
for m in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][m] * x[k] for k in range(NumProducts)]) <= AvailableTime[m], f"Machine_{m+1}_Time"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')