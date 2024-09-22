import pulp
import json

# Given data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0)

# Objective Function
problem += pulp.lpSum([price[p] * pulp.lpSum([output_data[l][p] * execute[l] for l in range(L)]) for p in range(P)])

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Output results
revenue = pulp.value(problem.objective)
execution_plan = [execute[l].varValue for l in range(L)]

print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
print(f'Execution Plan: {execution_plan}')