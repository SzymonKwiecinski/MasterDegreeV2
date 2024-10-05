import pulp

# Data extraction
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
p = data['Period']
demand = data['Demand']

# Problem definition
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables
x = {j: pulp.LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(T)}
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[j] for j in range(T)), "Minimize Total Nurses"

# Constraints
for k in range(T):
    problem += pulp.lpSum(x[(j % T)] for j in range(k, k + p)) >= demand[k], f"Demand_Constraint_day_{k+1}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')