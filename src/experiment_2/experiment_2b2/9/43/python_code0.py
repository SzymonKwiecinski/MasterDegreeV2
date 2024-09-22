import pulp

# Data from the problem
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Create a linear programming problem (maximize profit)
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of products
M = len(data['prices'])
# Number of materials
N = len(data['available'])

# Decision variables: amount to produce for each product
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=data['demands'][j], cat='Continuous') for j in range(M)]

# Objective function: Maximize profit
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * amount[j] for j in range(M))

# Constraints for raw materials availability
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(M)) <= data['available'][i], f'Material_{i}'

# Solve the problem
problem.solve()

# Extract the results
amount_produced = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Prepare the output in the requested format
output = {
    "amount": amount_produced,
    "total_profit": total_profit
}

# Printing the outputs
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')