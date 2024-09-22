import pulp

# Parse the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start)

# Constraints: meet the demand for each day
for j in range(T):
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare the result
start_values = [pulp.value(start[j]) for j in range(T)]
total_nurses = sum(start_values)

# Output the result
output = {
    "start": start_values,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')