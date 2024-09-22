import pulp
import json

# Loading data from JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Parameters
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of processes
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, L+1), lowBound=0)

# Objective function
revenue_terms = []
for l in range(1, L+1):
    term = pulp.lpSum((price[p-1] * output_matrix[l-1][p-1] - cost[l-1] * output_matrix[l-1][p-1]) * x[l] for p in range(1, P+1))
    revenue_terms.append(term)

problem += pulp.lpSum(revenue_terms), "Total_Revenue"

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_matrix[l-1][i] * x[l] for l in range(1, L+1)) <= allocated[i], f"Crude_Oil_Allocation_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')