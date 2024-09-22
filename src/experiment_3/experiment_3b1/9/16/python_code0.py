import pulp
import json

# Data in JSON format
data_json = '{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}'
data = json.loads(data_json)

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
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * execute[l] for l in range(L)) for p in range(P))
problem += revenue

# Constraints
# Constraint for allocated crude oil types
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Constraint for revenue - costs
problem += revenue - pulp.lpSum(cost[l] * pulp.lpSum(output_data[l][p] * execute[l] for p in range(P)) for l in range(L)) >= 0

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
execute_values = [execute[l].varValue for l in range(L)]
print(f'Optimal execution of processes: {execute_values}')