import pulp
import json

# Data
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables
execute = pulp.LpVariable.dicts("execute", range(data['L']), lowBound=0, cat='Continuous')

# Objective function
revenue_expr = pulp.lpSum(data['Price'][p] * pulp.lpSum(data['Output'][l][p] * execute[l] for l in range(data['L'])) for p in range(data['P']))
problem += revenue_expr, "Total_Revenue"

# Constraints
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * execute[l] for l in range(data['L'])) <= data['Allocated'][i], f"Crude_Oil_Allocation_{i+1}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')