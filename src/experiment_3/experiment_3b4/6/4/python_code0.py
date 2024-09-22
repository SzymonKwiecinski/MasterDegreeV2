import pulp

# Extract the relevant data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f"start_{j}", lowBound=0, cat='Integer') for j in range(T)]

# Objective function
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - i - 1) % T] for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')