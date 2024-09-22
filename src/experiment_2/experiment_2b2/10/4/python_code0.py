import pulp

# Data from the given JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extract parameters
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: start[j] represents the number of nurses starting their shift on day j
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat=pulp.LpInteger)

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints: Ensure demand is met for each day
for j in range(T):
    demand_constraint = pulp.lpSum(start[(j - t) % T] for t in range(Period))
    problem += demand_constraint >= Demand[j], f"Demand_Day_{j+1}"

# Solve the problem
problem.solve()

# Output the results
start_solution = [int(start[j].varValue) for j in range(T)]
total_nurses = int(pulp.value(problem.objective))

output = {
    "start": start_solution,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')