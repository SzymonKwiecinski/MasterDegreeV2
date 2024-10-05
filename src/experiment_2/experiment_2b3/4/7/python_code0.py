import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extract values from data
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
max_a = pulp.LpVariable("max_a", lowBound=0, cat='Continuous')

# Objective function
problem += max_a

# Constraints
problem += x[0] == x_0
problem += v[0] == v_0

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_a
    problem += -a[t] <= max_a

problem += x[T] == x_T
problem += v[T] == v_T

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "x": [pulp.value(x[i]) for i in range(1, T + 1)],
    "v": [pulp.value(v[i]) for i in range(1, T + 1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": sum(abs(pulp.value(a[i])) for i in range(T))
}

# Print output data
print(output)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')