import pulp

# Parse the input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Define the LP problem
problem = pulp.LpProblem("Rocket_Minimum_Thrust", pulp.LpMinimize)

# Define the decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
max_thrust = pulp.LpVariable("max_thrust", lowBound=0, cat='Continuous')

# Set the objective to minimize the maximum thrust
problem += max_thrust, "Minimize_Max_Thrust"

# Set the initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Set the target conditions
problem += (x[T] == x_T, "Target_Position")
problem += (v[T] == v_T, "Target_Velocity")

# Add constraints for the motion equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (a[t] <= max_thrust, f"Max_Thrust_Positive_{t}")
    problem += (-a[t] <= max_thrust, f"Max_Thrust_Negative_{t}")

# Solve the LP problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[t]) for t in range(1, T+1)]
v_values = [pulp.value(v[t]) for t in range(1, T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')