import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a LP minimization problem
problem = pulp.LpProblem("Minimum_Thrust_Rocket", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-1, upBound=1, cat='Continuous') for t in range(T)]  # Assuming |a_t| <= 1

# Objective Function: Minimize the maximum absolute thrust (acceleration)
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')
problem += M

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    # Limit the maximum thrust
    problem += (a[t] <= M, f"Max_Thrust_Upper_{t}")
    problem += (-a[t] <= M, f"Max_Thrust_Lower_{t}")

# Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=False))

# Collect the results
x_result = [pulp.value(x[t]) for t in range(T+1)]
v_result = [pulp.value(v[t]) for t in range(T+1)]
a_result = [pulp.value(a[t]) for t in range(T)]

# Calculate total fuel spent (sum of absolute accelerations)
fuel_spent = sum(abs(a_t) for a_t in a_result)

output = {
    "x": x_result[1:],
    "v": v_result[1:],
    "a": a_result,
    "fuel_spend": fuel_spent,
}

print(output)
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")