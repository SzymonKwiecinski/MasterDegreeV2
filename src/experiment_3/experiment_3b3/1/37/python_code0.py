import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Problem Initialization
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Sets
num_parts = len(data['profit'])
num_shops = len(data['capacity'])

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective Function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Constraints
for s in range(num_shops):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(num_parts)) <= data['capacity'][s], f"Capacity_Shop_{s}"

# Solving the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')