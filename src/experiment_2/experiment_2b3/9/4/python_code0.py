import pulp

# Parse the data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start)

# Constraints: Meet the demand for nurses each day
for j in range(T):
    problem += pulp.lpSum(start[(j-i) % T] for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Get the results
start_values = [int(pulp.value(start[j])) for j in range(T)]
total_nurses = int(pulp.value(problem.objective))

# Output the results
result = {
    "start": start_values,
    "total": total_nurses
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')