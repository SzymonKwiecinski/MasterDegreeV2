import pulp

# Extract data from JSON.
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the linear programming problem
problem = pulp.LpProblem("RocketMotionModel", pulp.LpMinimize)

# Declare the variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), cat="Continuous")

# Objective function: minimize the fuel consumption (sum of absolute values of a_t)
fuel_spend = pulp.lpSum(pulp.lpSum([pulp.lpSum([a[t] for t in range(T)]), -pulp.lpSum([-a[t] for t in range(T)])]))
problem += fuel_spend

# Constraints
# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Final conditions
problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Motion equations
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"MotionPosition_{t}")
    problem += (v[t+1] == v[t] + a[t], f"MotionVelocity_{t}")

# Solve the problem
problem.solve()

# Extract the solution
x_values = [pulp.value(x[i]) for i in range(T+1)]
v_values = [pulp.value(v[i]) for i in range(T+1)]
a_values = [pulp.value(a[i]) for i in range(T)]

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": pulp.value(problem.objective)
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')