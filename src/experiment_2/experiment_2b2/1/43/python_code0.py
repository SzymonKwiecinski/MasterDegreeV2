import pulp

# Data from input
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

N = len(available)  # number of raw materials
M = len(demands)    # number of products

# LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f"amount_{j}", lowBound=0, upBound=demands[j], cat='Integer') for j in range(M)]

# Objective function: Maximize total profit
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum([profit[j] * amount[j] for j in range(M)])

# Constraints
# Material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Output results
output = {
    "amount": [pulp.value(amount[j]) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')