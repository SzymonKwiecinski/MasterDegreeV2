import pulp

# Data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_parts = len(data['profit'])
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
profit = data['profit']
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Constraints
time = data['time']
capacity = data['capacity']
num_shops = len(time[0])

for s in range(num_shops):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Shop_{s}"

# Solve the problem
problem.solve()

# Output results
quantity_result = [pulp.value(quantity[k]) for k in range(num_parts)]
output = {"quantity": quantity_result}
print(output)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')