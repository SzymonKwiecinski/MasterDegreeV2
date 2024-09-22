import pulp
import json

# Data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create a linear programming problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables: number of times process l is executed
x = pulp.LpVariable.dicts("Process", range(L), lowBound=0)

# Objective function: Maximize total revenue
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l][p] * x[l] for l in range(L)) for p in range(P)) \
                  - pulp.lpSum(cost[l] * pulp.lpSum(output_matrix[l][p] * x[l] for p in range(P)) for l in range(L))

problem += revenue, "Total_Revenue"

# Constraints: The total input for each crude oil type must not exceed the allocated amount
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * x[l] for l in range(L)) <= allocated[i], f"Input_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')