import pulp

# Problem Data
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of products
M = len(data["prices"])
# Number of raw materials
N = len(data["available"])

# Decision variables: amount of each product to produce
amount = [pulp.LpVariable(f"amount_{j}", lowBound=0, cat='Integer') for j in range(M)]

# Objective function: maximize total profit
profit = pulp.lpSum([(data["prices"][j] - data["costs"][j]) * amount[j] for j in range(M)])
problem += profit

# Constraints for available raw materials
for i in range(N):
    problem += pulp.lpSum([data["requirements"][j][i] * amount[j] for j in range(M)]) <= data["available"][i]

# Constraints for maximum demand
for j in range(M):
    problem += amount[j] <= data["demands"][j]

# Solve the problem
problem.solve()

# Collect results
solution = {
    "amount": [int(amount[j].varValue) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')