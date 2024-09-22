import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products (M) and raw materials (N)
M = len(prices)
N = len(available)

# Initialize the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables: amount produced for each product
amounts = [pulp.LpVariable(f'amount_{j}', 0, demands[j]) for j in range(M)]

# Objective function: maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amounts[j] for j in range(M)])
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amounts[j] for j in range(M)]) <= available[i], f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Collect results
amounts_produced = [amounts[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output results
result = {
    "amount": amounts_produced,
    "total_profit": total_profit
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')