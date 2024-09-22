import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Variables
start = [pulp.LpVariable(f'start_{j+1}', lowBound=0, cat='Integer') for j in range(T)]

# Objective
problem += pulp.lpSum(start)

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[((j - i) % T)] for i in range(Period)) >= Demand[j]

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')