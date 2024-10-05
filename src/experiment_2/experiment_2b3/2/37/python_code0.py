import pulp

# Data input
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

time = data['time']
profit = data['profit']
capacity = data['capacity']

K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(K)])

# Constraints
for s in range(S):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(K)]) <= capacity[s]

# Solve the problem
problem.solve()

# Retrieve the solution
solution = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Print the solution
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')