import pulp

# Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extract data values
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Define the problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f"x_{t}", cat="Continuous") for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat="Continuous") for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", -1, 1, cat="Continuous") for t in range(T)]  # |a_t| <= 1

max_a = pulp.LpVariable("max_a", 0)

# Objective: Minimize maximum absolute acceleration
problem += max_a

# Constraints
# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (max_a >= a[t], f"Max_Constraint_Positive_{t}")
    problem += (max_a >= -a[t], f"Max_Constraint_Negative_{t}")

# Solve the problem
problem.solve()

# Prepare the outputs
result = {
    "x": [pulp.value(x[t]) for t in range(1, T + 1)],
    "v": [pulp.value(v[t]) for t in range(1, T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": sum(abs(pulp.value(a[t])) for t in range(T))
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')