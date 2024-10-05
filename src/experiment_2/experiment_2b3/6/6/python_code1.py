import pulp

# Parse the data from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the LP problem
problem = pulp.LpProblem("RocketPathOptimization", pulp.LpMinimize)

# Declare decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Auxiliary variables for absolute value of acceleration
a_pos = [pulp.LpVariable(f"a_pos_{t}", cat='Continuous') for t in range(T)]
a_neg = [pulp.LpVariable(f"a_neg_{t}", cat='Continuous') for t in range(T)]

# Objective function: Minimize the total fuel (sum of absolute acceleration)
problem += pulp.lpSum(a_pos[t] + a_neg[t] for t in range(T))

# Constraints for the absolute value of acceleration
for t in range(T):
    problem += (a_pos[t] >= a[t], f"pos_constraint_{t}")
    problem += (a_neg[t] >= -a[t], f"neg_constraint_{t}")

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"position_constraint_t{t}")
    problem += (v[t + 1] == v[t] + a[t], f"velocity_constraint_t{t}")

# Solve the problem
problem.solve()

# Construct the output
output = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the resulting objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')