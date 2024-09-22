import pulp
import json

data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data from json
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit, "Total_Profit"

# Constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i], f"Material_{i+1}"

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_{j+1}"

# Solve the problem
problem.solve()

# Prepare the output
amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

# Output format
output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(json.dumps(output))