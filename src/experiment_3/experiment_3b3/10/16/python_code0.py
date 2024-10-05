import pulp

# Data from the JSON
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

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output[l][p] * x[l] for l in range(L)) for p in range(P))
cost_total = pulp.lpSum(cost[l] * pulp.lpSum(output[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - cost_total, "Total Revenue"

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"Crude_Allocation_{i}"

# Solve the problem
problem.solve()

# Output results
execute_times = {f'Process_{l+1}': pulp.value(x[l]) for l in range(L)}
total_revenue = pulp.value(problem.objective)

print("Execute times for each process:")
for process, times in execute_times.items():
    print(f"{process}: {times}")

print(f"Total Revenue (Objective Value): <OBJ>{total_revenue}</OBJ>")