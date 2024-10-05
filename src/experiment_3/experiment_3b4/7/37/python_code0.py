import pulp

# Data from JSON
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts (K) and shops (S)
K = len(profit)
S = len(capacity)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{k+1}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')