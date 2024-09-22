import pulp

# Parse the data
data = {
    'available': [240000, 8000, 75000], 
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
    'prices': [40, 38, 9], 
    'costs': [30, 26, 7], 
    'demands': [10000, 2000, 10000]
}

available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and materials
M = len(prices)
N = len(available)

# Create a linear programming problem
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Decision variables
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demands[j], cat='Continuous') for j in range(M)]

# Objective function: Maximize total profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amounts[j] for j in range(M)])
problem += profit

# Constraints: Raw material availability
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amounts[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Output the results
output = {
    'amount': [pulp.value(amounts[j]) for j in range(M)],
    'total_profit': pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')