import pulp

# Data provided in JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Unpack data
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of spare parts (K) and shops (S)
K = len(profit)
S = len(capacity)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]

# Solve the problem
problem.solve()

# Output the optimal quantities of each spare part to be produced
optimal_quantities = [pulp.value(quantity[k]) for k in range(K)]
print(f'Optimal Quantities: {optimal_quantities}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')