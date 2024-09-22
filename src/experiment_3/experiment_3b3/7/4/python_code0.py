import pulp

# Data from the JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extract data
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([x[j] for j in range(T)])

# Constraints
for j in range(T):
    problem += pulp.lpSum([x[(j-k) % T] for k in range(period)]) >= demand[j]

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Fetch results
start = [pulp.value(x[j]) for j in range(T)]
total = pulp.value(problem.objective)

# Print the results
print(f"(Start): {start}")
print(f"(Total Nurses): {total}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')