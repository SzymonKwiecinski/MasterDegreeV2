import pulp

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Parse data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']
num_parts = data['NumParts']
num_machines = data['NumMachines']

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(num_parts)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Constraints
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_Shop_{s+1}"

# Solve problem
problem.solve()

# Collect results
quantity_result = [pulp.value(quantity[k]) for k in range(num_parts)]

# Output Format
output = {
    "quantity": quantity_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')