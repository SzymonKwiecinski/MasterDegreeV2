import pulp

# Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create a MILP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Extract results
start_counts = [int(start[j].varValue) for j in range(T)]
total_nurses = sum(start_counts)

# Output format
output = {
    "start": start_counts,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')