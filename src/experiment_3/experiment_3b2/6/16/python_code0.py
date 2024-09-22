import pulp
import json

# Data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting the data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

# Objective Function
revenue = pulp.lpSum([price[p] * pulp.lpSum([output_matrix[l][p] * execute[l] for l in range(L)]) for p in range(P)]) \
                     - pulp.lpSum([cost[l] * pulp.lpSum([output_matrix[l][p] * execute[l] for p in range(P)]) for l in range(L)])
problem += revenue

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_matrix[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')