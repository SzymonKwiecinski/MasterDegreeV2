import pulp

# Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start)

# Constraints
for j in range(T):
    # Determine the number of nurses working on each day j
    nurses_working = sum(start[(j - k) % T] for k in range(period))
    # Ensure the demand is met
    problem += nurses_working >= demand[j]

# Solve the problem
problem.solve()

# Extract the results
start_schedule = [int(pulp.value(start[j])) for j in range(T)]
total_nurses = pulp.value(problem.objective)

# Output
output = {
    "start": start_schedule,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')