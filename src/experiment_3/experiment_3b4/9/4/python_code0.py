import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j+1}', lowBound=0, cat='Integer') for j in range(T)]

# Objective Function
problem += pulp.lpSum(x[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j-i-1) % T] for i in range(period)) >= demand[j]

# Solve
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')