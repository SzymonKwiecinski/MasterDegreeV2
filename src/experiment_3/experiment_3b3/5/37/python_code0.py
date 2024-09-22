import pulp

# Extracting data from the provided JSON-like format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Define the Linear Programming problem
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Shop_{s+1}"

# Solve the problem
problem.solve()

# Objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")