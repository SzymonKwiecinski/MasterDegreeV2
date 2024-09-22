import pulp

# Data from JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j}', cat='Integer', lowBound=0) for j in range(T)]

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start)

# Constraints
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j])

# Solve the problem
problem.solve()

# Results
start_values = [int(start[j].varValue) for j in range(T)]
total_nurses = int(sum(start_values))

# Print output in specified format
output = {
    "start": start_values,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')