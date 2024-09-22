import pulp

# Read data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective
problem += total

# Constraints
problem += total == pulp.lpSum([start[j] for j in range(T)])

for j in range(T):
    problem += pulp.lpSum([start[(j-i) % T] for i in range(period)]) >= demand[j]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')