import pulp

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Extract data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Define decision variables
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start)

# Add constraints for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j-p) % T] for p in range(Period)) >= Demand[j])

# Solve the problem
problem.solve()

# Retrieve the results
output = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')