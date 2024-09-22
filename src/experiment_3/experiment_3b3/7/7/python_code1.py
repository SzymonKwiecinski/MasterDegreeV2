import pulp

# Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extract data
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]
a_abs = [pulp.LpVariable(f'a_abs_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective: Minimize the maximum absolute thrust
problem += pulp.lpSum(a_abs), "Minimize_Maximum_Thrust"

# Initial conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

# Dynamics and constraints over time
for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"Position_Dynamics_at_{t}"
    problem += v[t+1] == v[t] + a[t], f"Velocity_Dynamics_at_{t}"
    problem += a_abs[t] >= a[t], f"Absolute_acceleration_positive_at_{t}"
    problem += a_abs[t] >= -a[t], f"Absolute_acceleration_negative_at_{t}"

# Final conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Solve the problem
problem.solve()

# Extract results
x_result = [pulp.value(x_t) for x_t in x]
v_result = [pulp.value(v_t) for v_t in v]
a_result = [pulp.value(a_t) for a_t in a]
fuel_spend = sum(abs(a_i) for a_i in a_result)

# Print results
print(f"x = {x_result}")
print(f"v = {v_result}")
print(f"a = {a_result}")
print(f"fuel_spend = {fuel_spend}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')