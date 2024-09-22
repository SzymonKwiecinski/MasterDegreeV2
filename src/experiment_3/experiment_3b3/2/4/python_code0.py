import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints
for k in range(T):
    problem += pulp.lpSum(start[j] * ((j <= k < j + period) or (j <= k % T < (j + period) % T)) for j in range(T)) >= demand[k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')