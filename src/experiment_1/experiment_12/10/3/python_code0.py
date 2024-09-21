import pulp

# Data from the problem
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumParts'])), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(data['NumMachines']):
    problem += (pulp.lpSum(data['Time'][k][s] * x[k] for k in range(data['NumParts'])) <= data['Capacity'][s]), f"Capacity_Constraint_Machine_{s+1}"

# Solve the problem
problem.solve()

# Print results
for k in range(data['NumParts']):
    print(f'Quantity of spare part {k+1} to produce: {x[k].varValue}')

# Objective function value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')