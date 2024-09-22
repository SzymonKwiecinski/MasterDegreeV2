import pulp
import json

# Data from the provided JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Defining the sets
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of production processes

# Defining the parameters
allocated = data['Allocated']  # allocated crude oil
price = data['Price']  # selling price per barrel of product
input_data = data['Input']  # barrels of crude needed for process
output_data = data['Output']  # barrels of product produced by process
cost = data['Cost']  # cost per barrel for process

# Create a problem variable
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision variables
execute = pulp.LpVariable.dicts("execute", range(1, L + 1), lowBound=0)

# Objective Function
total_revenue = pulp.lpSum(price[p - 1] * pulp.lpSum(output_data[l - 1][p - 1] * execute[l] for l in range(1, L + 1)) for p in range(1, P + 1))
total_cost = pulp.lpSum(cost[l - 1] * pulp.lpSum(output_data[l - 1][p - 1] * execute[l] for p in range(1, P + 1)) for l in range(1, L + 1))
problem += total_revenue - total_cost, "Total_Profit"

# Supply constraints for each crude oil type
for i in range(1, O + 1):
    problem += (pulp.lpSum(input_data[l - 1][i - 1] * execute[l] for l in range(1, L + 1)) <= allocated[i - 1]), f"Supply_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')