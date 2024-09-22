import pulp

# Data from the provided JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Define sets
T = range(len(data['demand']))  # Time periods
K = range(len(data['num']))      # Generator types

# Create the problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (k for k in K for t in T), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", (k for k in K for t in T), lowBound=0, upBound=None)
startup = pulp.LpVariable.dicts("startup", (k for k in K for t in T), cat='Binary')

# Objective function
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] +
                       data['startcost'][k] * startup[k, t] +
                       data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t]
                       for k in K for t in T), "Total_Cost"

# Constraints

# Load Demand Constraint
for t in T:
    problem += pulp.lpSum(level[k, t] * numon[k, t] for k in K) >= data['demand'][t], f"Load_Demand_Constraint_{t}"

# Generator Capacity Constraints
for k in K:
    for t in T:
        problem += level[k, t] >= data['minlevel'][k] * numon[k, t], f"Min_Capacity_Constraint_k{k}_t{t}"
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t], f"Max_Capacity_Constraint_k{k}_t{t}"

# Generator Availability Constraints
for k in K:
    for t in T:
        problem += numon[k, t] <= data['num'][k], f"Availability_Constraint_k{k}_t{t}"

# Startup Constraints
for k in K:
    for t in T:
        problem += level[k, t] >= data['minlevel'][k] * startup[k, t], f"Startup_Constraint_k{k}_t{t}"

# Solve the problem
problem.solve()

# Output results
numon_output = {k: [numon[k, t].varValue for t in T] for k in K}
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Generated output (numon):", numon_output)