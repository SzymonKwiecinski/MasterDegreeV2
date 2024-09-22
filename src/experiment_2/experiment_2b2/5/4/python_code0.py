import pulp

# Parse the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize total number of nurses
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Extract results
start_values = [int(pulp.value(start[j])) for j in range(T)]
total_nurses = sum(start_values)

# Output format
output = {
    "start": start_values,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')