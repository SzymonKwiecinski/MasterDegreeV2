import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Number of products and raw materials
M = len(data['prices'])
N = len(data['available'])

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=data['demands'][j], cat='Continuous') for j in range(M)]

# Objective Function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M))
problem += profit

# Constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(M)) <= data['available'][i]

# Solve the problem
problem.solve()

# Prepare results
amounts = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    'amount': amounts,
    'total_profit': total_profit
}

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')