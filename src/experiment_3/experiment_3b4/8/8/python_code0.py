import pulp

# Parse data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

# Objective function
profit = data['Profit']
problem += pulp.lpSum(profit[k] * x[k] for k in range(data['NumParts']))

# Constraints
time = data['Time']
capacity = data['Capacity']

# Capacity constraints for each machine
for s in range(data['NumMachines']):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(data['NumParts'])) <= capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')