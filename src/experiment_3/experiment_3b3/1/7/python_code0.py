import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(data['T'] + 1), lowBound=None, cat='Continuous')
a = pulp.LpVariable.dicts("a", range(data['T']), lowBound=None, cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

# Objective
problem += M, "Minimize maximum thrust"

# Constraints
problem += (x[0] == data['X0']), "Initial position"
problem += (v[0] == data['V0']), "Initial velocity"
problem += (x[data['T']] == data['XT']), "Target position"
problem += (v[data['T']] == data['VT']), "Target velocity"

# Dynamics constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t]), f"Position update at time {t}"
    problem += (v[t + 1] == v[t] + a[t]), f"Velocity update at time {t}"
    problem += (pulp.lpSum([a[t]]) <= M), f"Maximum thrust {t}"
    problem += (pulp.lpSum([-a[t]]) <= M), f"Minimum thrust {-t}"

# Solve problem
problem.solve()

# Output results
x_values = [pulp.value(x[t]) for t in range(data['T'] + 1)]
v_values = [pulp.value(v[t]) for t in range(data['T'] + 1)]
a_values = [pulp.value(a[t]) for t in range(data['T'])]
fuel_spend = sum(abs(av) for av in a_values)

print("Positions:", x_values)
print("Velocities:", v_values)
print("Accelerations:", a_values)
print("Fuel Spend:", fuel_spend)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')