import pulp

# Reading data from the input
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

# Number of products (M) and number of materials (N)
M = len(data["prices"])
N = len(data["available"])

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of each product to produce
amount = [pulp.LpVariable(f"amount_{j}", lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: maximize total profit
profit = pulp.lpSum((data["prices"][j] - data["costs"][j]) * amount[j] for j in range(M))
problem += profit

# Constraints: Raw material availability constraints
for i in range(N):
    problem += pulp.lpSum(data["requirements"][j][i] * amount[j] for j in range(M)) <= data["available"][i], f"Material_{i}_Constraint"

# Demand constraints: Cannot exceed forecasted maximum demand
for j in range(M):
    problem += amount[j] <= data["demands"][j], f"Demand_{j}_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount[j]) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

# Display the result
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')