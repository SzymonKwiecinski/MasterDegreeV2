import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Minimum_Thrust", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
max_a = pulp.LpVariable("max_a", lowBound=0, cat='Continuous')

# Objective: Minimize maximum thrust
problem += max_a, "Minimize_Max_Acceleration"

# Constraints

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# State equations
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (a[t] <= max_a, f"Max_Acceleration_Positive_{t}")
    problem += (-a[t] <= max_a, f"Max_Acceleration_Negative_{t}")

# Solve the problem
problem.solve()

# Extract the results
trajectory_x = [pulp.value(x[t]) for t in range(1, T + 1)]
trajectory_v = [pulp.value(v[t]) for t in range(1, T + 1)]
trajectory_a = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Prepare the output
output = {
    "x": trajectory_x,
    "v": trajectory_v,
    "a": trajectory_a,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')