import pulp
import json

# Given data in JSON format
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extracting the provided data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and resources
M = len(prices)
N = len(available)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demands[j]) for j in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints for each raw material
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i], f"Resource_Constraint_{i}"

# Solve the problem
problem.solve()

# Results
produced_amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "amount": produced_amounts,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')