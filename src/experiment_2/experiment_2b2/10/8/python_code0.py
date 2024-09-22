import pulp

# Parse the input data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective Function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantities[k] for k in range(num_parts)])

# Constraints: Each machine's capacity
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantities[k] for k in range(num_parts)]) <= capacity[s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Extract the solution
output = {"quantity": [pulp.value(quantities[k]) for k in range(num_parts)]}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')