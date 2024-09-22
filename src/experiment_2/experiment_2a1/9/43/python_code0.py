import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Number of products and materials
M = len(data['prices'])
N = len(data['available'])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define the decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M)), "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(M)) <= data['available'][i], f"Material_Constraint_{i}"

# Constraints for demand
for j in range(M):
    problem += amount[j] <= data['demands'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print the results
output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')