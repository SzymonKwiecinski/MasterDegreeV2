import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], 
                        [40, 1, 10], 
                        [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: amount of each product produced
amount = pulp.LpVariable.dicts("amount", range(len(data['prices'])), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(len(data['prices'])))
problem += profit

# Constraints for raw materials
for i in range(len(data['available'])):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(len(data['requirements']))) <= data['available'][i]

# Constraints for maximum demands
for j in range(len(data['demands'])):
    problem += amount[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Prepare output
amount_produced = [amount[j].varValue for j in range(len(data['prices']))]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "amount": amount_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')