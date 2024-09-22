import json
import pulp

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Number of products and raw materials
M = len(data['prices'])
N = len(data['available'])

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function: Maximize profit
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M))
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(M)) <= data['available'][i]

# Constraints for demands
for j in range(M):
    problem += amount[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "amount": [amount[j].varValue for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

# Print output
print(f' (Objective Value): <OBJ>{output["total_profit"]}</OBJ>')