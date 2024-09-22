import pulp

data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Additional variable to represent max thrust
max_thrust = pulp.LpVariable("max_thrust", lowBound=0, cat='Continuous')

# Objective function: minimize the maximum thrust
problem += max_thrust

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Constraints for the motion equations
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]

# Thrust constraints
for t in range(T):
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

# Solve the problem
problem.solve()

# Extract results
output = {
    "x": [pulp.value(x_var) for x_var in x],
    "v": [pulp.value(v_var) for v_var in v],
    "a": [pulp.value(a_var) for a_var in a],
    "fuel_spend": sum(abs(pulp.value(a_var)) for a_var in a)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')