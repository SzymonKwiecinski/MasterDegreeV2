import pulp

# Data from JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem definition
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function
problem += pulp.lpSum(x[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[j - i] if j - i >= 0 else 0 for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Collect results
start = [pulp.value(x[j]) for j in range(T)]

# Print the results
print("Number of nurses starting each day:", start)
print(f"Total number of nurses hired (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")