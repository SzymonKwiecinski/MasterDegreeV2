import pulp
import json

data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)  # number of products
N = len(available)  # number of raw materials

# Create the LP problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, cat='Continuous')

# Objective function: maximize profit
profit = pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M))
problem += profit

# Constraints for available raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]

# Constraints for maximum demand
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Gather results
result_amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "amount": result_amounts,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')