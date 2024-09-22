import pulp

# Parse the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Shift_Allocation", pulp.LpMinimize)

# Variables: number of nurses starting their period on each day
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Objective: Minimize the total number of nurses
problem += pulp.lpSum(start)

# Constraints: Meet the demand for each day
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(Period)) >= Demand[j], f"Demand_constraint_day_{j}"

# Solve the problem
problem.solve()

# Gather results
result = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Output the results
print(result)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")