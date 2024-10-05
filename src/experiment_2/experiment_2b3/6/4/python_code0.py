import pulp

# Extract data from JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: start[j] where j is the day a nurse starts their shift
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints: Fulfill the demand for each day
for j in range(T):
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Gather output data
start_values = [int(start[j].varValue) for j in range(T)]
total_nurses = sum(start_values)

# Output results
output = {
    "start": start_values,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')