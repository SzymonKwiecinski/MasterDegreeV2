import pulp

# Given data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
    'prices': [40, 38, 9], 
    'costs': [30, 26, 7], 
    'demands': [10000, 2000, 10000]
}

# Extracting values from the data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and raw materials
M = len(prices)
N = len(available)

# Profit coefficients for each product
profit_coeffs = [prices[j] - costs[j] for j in range(M)]

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize profit
problem += pulp.lpSum([profit_coeffs[j] * amount[j] for j in range(M)]), "Total_Profit"

# Constraints
# Material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i], f"Material_{i}_Availability"

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_{j}_Constraint"

# Solve the problem
problem.solve()

# Collect results
result_amount = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

output = {
    "amount": result_amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')