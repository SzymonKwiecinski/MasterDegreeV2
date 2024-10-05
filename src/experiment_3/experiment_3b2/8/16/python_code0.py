import pulp

# Data from the provided JSON
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

# Extracting the parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(L), lowBound=0)

# Objective function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output[l][p] * x[l] for l in range(L)) for p in range(P))
costs = pulp.lpSum(cost[l] * pulp.lpSum(output[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - costs, "Total_Revenue"

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"Allocation_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')