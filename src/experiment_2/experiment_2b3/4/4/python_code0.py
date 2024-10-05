import pulp

# Parsing data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize problem
problem = pulp.LpProblem("Minimize_Nurses", pulp.LpMinimize)

# Decision variables
start_nurses = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize total number of nurses
total_nurses = pulp.lpSum(start_nurses)
problem += total_nurses

# Constraints
for j in range(T):
    # Sum of nurses covering day j
    nurses_covering_j = pulp.lpSum(start_nurses[(j - i) % T] for i in range(period))
    problem += (nurses_covering_j >= demand[j], f"demand_constraint_{j}")

# Solve the problem
problem.solve()

# Extract results
schedule = [int(start_nurses[j].varValue) for j in range(T)]
total_hired = int(pulp.value(total_nurses))

# Print results
output = {
    "start": schedule,
    "total": total_hired
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')