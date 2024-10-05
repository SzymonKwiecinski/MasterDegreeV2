import pulp

# Problem data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Parameters
T = data["T"]
Period = data["Period"]
Demand = data["Demand"]

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start_vars = [pulp.LpVariable(f'start_{j}', cat='Integer', lowBound=0) for j in range(T)]

# Objective function: Minimize total number of nurses
problem += pulp.lpSum(start_vars)

# Constraints: Meeting daily nurse demand
for j in range(T):
    # Calculate available nurses for each day
    nurses_available = sum(start_vars[(j-i) % T] for i in range(Period))
    problem += nurses_available >= Demand[j]

# Solve the problem
problem.solve()

# Prepare the result
start = [int(pulp.value(start_vars[j])) for j in range(T)]
total = sum(start)

# Output format
result = {
    "start": start,
    "total": total
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')