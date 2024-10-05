import pulp

# Input data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Extract the results
quantity_result = [pulp.value(quantity[k]) for k in range(K)]

# Output result
output = {
    "quantity": quantity_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')