import pulp

data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Initialize problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Extract data
x_0, v_0, x_T, v_T, T = data['X0'], data['V0'], data['XT'], data['VT'], data['T']

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
delta = pulp.LpVariable("delta", lowBound=0, cat='Continuous')

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Terminal conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# System dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Objective function
problem += delta

# Constraints for minimizing the maximum absolute acceleration (thrust)
for t in range(T):
    problem += (a[t] <= delta)
    problem += (-a[t] <= delta)

# Solve problem
problem.solve()

# Extract results
positions = [pulp.value(x_t) for x_t in x]
velocities = [pulp.value(v_t) for v_t in v]
accelerations = [pulp.value(a_t) for a_t in a]
fuel_spent = sum(abs(pulp.value(a_t)) for a_t in a)

# Output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')