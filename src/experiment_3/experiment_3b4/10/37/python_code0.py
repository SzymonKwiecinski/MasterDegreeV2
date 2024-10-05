import pulp

# Extracting data from the JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of spare parts
K = len(profit)

# Number of shops
S = len(capacity)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([profit[k] * x[k] for k in range(K)]), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum([time[k][s] * x[k] for k in range(K)]) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')