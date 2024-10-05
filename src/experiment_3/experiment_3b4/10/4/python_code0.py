import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
starts = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function
problem += pulp.lpSum(starts)

# Constraints
for j in range(T):
    problem += pulp.lpSum(starts[i % T] for i in range(j - period + 1, j + 1)) >= demand[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')