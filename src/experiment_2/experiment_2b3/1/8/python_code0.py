import pulp

# Data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each part to be made
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

# Constraints: Capacity constraints for each machine
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s], f"Capacity_Constraint_Machine_{s+1}"

# Solve the problem
problem.solve()

# Extract the quantities solution
solution = {"quantity": [pulp.value(quantity[k]) for k in range(num_parts)]}

# Output the solution
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')