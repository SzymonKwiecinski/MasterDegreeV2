import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables: Number of nurses starting on each day (integer and non-negative)
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

# Objective: Minimize the total number of nurses hired
problem += pulp.lpSum([start[j] for j in range(1, T + 1)])

# Constraints: Ensure the demand on each day is met
for j in range(1, T + 1):
    problem += pulp.lpSum([start[(j-i-1) % T + 1] for i in range(period)]) >= demand[j-1], f"Demand_Day_{j}"

# Solve
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')