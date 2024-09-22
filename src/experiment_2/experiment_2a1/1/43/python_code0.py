import pulp
import json

# Input data in JSON format
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data from the input
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and raw materials
M = len(prices)
N = len(available)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demand) for j, demand in enumerate(demands)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Prepare output
amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print the result in the specified format
output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(json.dumps(output))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')