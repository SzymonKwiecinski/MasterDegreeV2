import pulp

# Defining the data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(K)]

# Objective function: Maximize profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(K)]), "Total_Profit"

# Constraints: Do not exceed shop capacities
for s in range(S):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(K)]) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Gather the results
output = {"quantity": [pulp.value(quantity[k]) for k in range(K)]}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')