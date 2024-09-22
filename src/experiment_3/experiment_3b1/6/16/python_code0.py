import pulp
import json

# Given data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting data from the JSON
O = data['O']  # number of crude oil types
P = data['P']  # number of products
L = data['L']  # number of production processes
allocated = data['Allocated']  # amount of crude oil allocated
price = data['Price']  # selling price of products
input_data = data['Input']  # input crude oil required for processes
output_data = data['Output']  # output products from processes
cost = data['Cost']  # cost per barrel of product produced

# Creating the LP problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables: number of times each process is executed
x = pulp.LpVariable.dicts("x", range(L), lowBound=0)

# Objective function: Maximize revenue - cost
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * x[l] for l in range(L)) for p in range(P))
total_cost = pulp.lpSum(cost[l] * pulp.lpSum(output_data[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - total_cost

# Constraints: Crude oil constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"CrudeOilConstraint_{i}"

# Non-negativity constraints are handled by defining the lowBound=0 in the variables

# Solving the problem
problem.solve()

# Output the results
revenue_value = pulp.value(problem.objective)
execution_plan = {l: x[l].varValue for l in range(L)}

print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')
print('Execution Plan:', execution_plan)