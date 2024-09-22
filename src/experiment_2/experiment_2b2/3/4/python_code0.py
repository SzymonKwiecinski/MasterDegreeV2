import pulp

# Parse the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create a MILP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Constraints
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f"DemandConstraint_{j}")

# Objective function
problem += pulp.lpSum(start)

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
output