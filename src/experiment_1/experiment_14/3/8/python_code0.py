import pulp

# Data from JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Parameters
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumProducts)])

# Constraints
# Production time constraints for each machine
for m in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][m] * x[k] for k in range(NumProducts)]) <= AvailableTime[m], f'Machine_{m}_Time'

# Solve the problem
problem.solve()

# Print the results
for k in range(NumProducts):
    print(f'Quantity of product {k+1} to be produced: {x[k].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')