import pulp

# Data extraction from JSON format
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(num_parts))

# Constraints - Capacity for each machine
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')