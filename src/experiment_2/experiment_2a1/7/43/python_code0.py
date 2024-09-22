import pulp
import json

data = {'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}

# Extracting data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Constraints for demands
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Extracting results
result_amount = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "amount": result_amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')