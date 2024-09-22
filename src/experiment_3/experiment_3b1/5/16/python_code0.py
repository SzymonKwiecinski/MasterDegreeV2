import pulp
import json

# Data input
data = '{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}'
data = json.loads(data)

# Parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Problem Definition
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Process", range(L), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([price[p] * pulp.lpSum([output_data[l][p] * x[l] for l in range(L)]) for p in range(P)])

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * x[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for l in range(L):
    print(f'Process {l + 1} execution count: {x[l].varValue}')