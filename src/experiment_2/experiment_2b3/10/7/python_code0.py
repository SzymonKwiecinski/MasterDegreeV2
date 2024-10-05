import pulp

# Data from the input
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Define parameters from the input data
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Control_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')  # Maximum thrust

# Objective function
problem += M, "Minimize_Maximum_Thrust"

# Constraints
problem += x[0] == x_0, "Initial_Position"
problem += v[0] == v_0, "Initial_Velocity"
problem += x[T] == x_T, "Target_Position"
problem += v[T] == v_T, "Target_Velocity"

for t in range(T):
    # Dynamic model constraints
    problem += x[t + 1] == x[t] + v[t], f"Position_Update_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}"

    # Thrust magnitude constraints
    problem += a[t] <= M, f"Positive_Thrust_Bound_{t}"
    problem += -a[t] <= M, f"Negative_Thrust_Bound_{t}"

# Solve the problem
problem.solve()

# Prepare the output
positions = [pulp.value(x[t]) for t in range(1, T + 1)]
velocities = [pulp.value(v[t]) for t in range(1, T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Output format
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')