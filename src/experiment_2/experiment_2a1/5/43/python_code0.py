import pulp
import json

# Input data
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of each product to produce
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0, upBound=demands, cat='Continuous')

# Objective function: maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amounts[j] for j in range(M)])
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amounts[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Extract results
amount_produced = [amounts[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "amount": amount_produced,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')