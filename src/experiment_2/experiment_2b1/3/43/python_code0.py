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

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, upBound=None, cat='Continuous')

# Objective function: Maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M))
problem += profit, "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"Material_Constraint_{i}"

# Constraints for demand
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

output = {
    "amount": amounts,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>') 