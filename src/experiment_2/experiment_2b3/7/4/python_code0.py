import pulp

# Define problem data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Define periods and demand
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: start[j] is the number of nurses starting on day j
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Objective function: minimize the total number of nurses
problem += pulp.lpSum(start)

# Constraints: for each day j, ensure the demand is satisfied
for j in range(T):
    problem += pulp.lpSum(start[(j - k + T) % T] for k in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Extract the results
start_values = [pulp.value(start[j]) for j in range(T)]
total_nurses = sum(start_values)

# Print the results in specified format
result = {
    "start": start_values,
    "total": total_nurses
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')