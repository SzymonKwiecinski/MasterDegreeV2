import pulp

# Data from the JSON format
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting the data
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each part to be made
quantities = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective Function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantities[k] for k in range(num_parts)])

# Constraints: Capacity constraints for each shop
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantities[k] for k in range(num_parts)]) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Extracting the solution
solution = {"quantity": [quantities[k].varValue for k in range(num_parts)]}

# Printing the solution and objective value
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')