import pulp

# Given data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting the data
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

# Constraints
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s]

# Solve
problem.solve()

# Results
quantity_result = [pulp.value(q) for q in quantity]

# Output
output = {
    "quantity": quantity_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')