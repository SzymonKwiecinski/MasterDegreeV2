import pulp

# Problem data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Problem parameters
M = len(data['prices'])  # Number of products
N = len(data['available'])  # Number of raw materials

# Decision variables for the amount produced of each product
amount_vars = [
    pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)
]

# Objective function: Maximize Profit
# Profit = Sum((Price[j] - Cost[j]) * Amount[j])
profit = pulp.lpSum(
    (data['prices'][j] - data['costs'][j]) * amount_vars[j] for j in range(M)
)
problem += profit

# Constraints
# Raw material availability constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount_vars[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += amount_vars[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Prepare the result in the specified format
result = {
    "amount": [pulp.value(amount_vars[j]) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')