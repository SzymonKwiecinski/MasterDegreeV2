import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extracting data from JSON
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(M), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M))
problem += profit, "Total_Profit"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"Raw_Material_{i+1}_Constraint"

for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Collecting results
amount_produced = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output results in the required format
output = {
    "amount": amount_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')