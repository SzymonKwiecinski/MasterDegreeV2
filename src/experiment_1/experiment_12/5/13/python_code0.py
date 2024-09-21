import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extract data
Time = data['time']
Profit = data['profit']
Capacity = data['capacity']

# Number of different spare parts
K = len(Profit)

# Number of machines
S = len(Capacity)

# Define the problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(K)])

# Constraints
# Machine capacity constraints
for s in range(S):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(K)]) <= Capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')