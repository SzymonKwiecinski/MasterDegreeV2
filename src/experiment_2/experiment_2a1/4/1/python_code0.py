import pulp
import json

# Input data in JSON format
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                        [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

# Model initialization
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: amount of each good produced
amounts = pulp.LpVariable.dicts("amount", range(data['M']), lowBound=0)

# Objective function: maximize total revenue
problem += pulp.lpSum(data['Prices'][j] * amounts[j] for j in range(data['M'])), "Total Revenue"

# Constraints based on raw material availability
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][j][i] * amounts[j] for j in range(data['M'])) <= data['Available'][i]), f"Material_{i+1}_Constraint"

# Solve the problem
problem.solve()

# Output the results
amounts_produced = [amounts[j].varValue for j in range(data['M'])]
result = {"amount": amounts_produced}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')