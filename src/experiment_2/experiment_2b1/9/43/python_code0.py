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

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables for the amount of each product produced
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demands[j]) for j in range(M)]

# Objective function: maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * amounts[j] for j in range(M))
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Gather results
amounts_produced = [amounts[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output the results
result = {
    "amount": amounts_produced,
    "total_profit": total_profit
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')