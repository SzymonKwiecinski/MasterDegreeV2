import pulp

# Data from the JSON format
data = {
    "time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    "profit": [30, 20, 40, 25, 10],
    "capacity": [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables for quantities of each spare part
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints: Each shop capacity
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]

# Solve the problem
problem.solve()

# Retrieve the results
result = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')