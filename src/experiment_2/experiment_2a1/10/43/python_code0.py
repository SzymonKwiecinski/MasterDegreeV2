import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extracting data from the input
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demands[j]) for j in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints
for i in range(N):
    problem += (pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]), f"Material_{i}_constraint"

# Solve the problem
problem.solve()

# Prepare output
amounts_produced = [pulp.value(amount[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print the result in the requested format
output = {
    "amount": amounts_produced,
    "total_profit": total_profit
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')