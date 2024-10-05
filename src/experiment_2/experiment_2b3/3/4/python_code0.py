import pulp

# Parse input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create a MILP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables for number of nurses starting on day j
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective: Minimize the total number of nurses hired
total_nurses = pulp.lpSum(start[j] for j in range(T))
problem += total_nurses

# Constraints: Ensure demand is met for each day
for j in range(T):
    # Calculate number of nurses available on day j
    available_nurses = sum(start[(j - k) % T] for k in range(period))
    problem += available_nurses >= demand[j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "start": [int(pulp.value(start[j])) for j in range(T)],
    "total": int(pulp.value(total_nurses))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')