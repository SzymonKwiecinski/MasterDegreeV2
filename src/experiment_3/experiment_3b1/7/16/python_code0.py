import pulp
import json

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

# Problem definition
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function
revenue = pulp.lpSum(price[p] * pulp.lpSum(x[l] * output_data[l][p] for l in range(L)) for p in range(P))
costs = pulp.lpSum(x[l] * cost[l] for l in range(L))
problem += revenue - costs

# Constraints
for i in range(O):
    problem += pulp.lpSum(x[l] * input_data[l][i] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')