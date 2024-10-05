import pulp

# Parsing Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Initialize the Linear Program
problem = pulp.LpProblem("Rocket_Control", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-1, upBound=1, cat='Continuous') for t in range(T)]
fuel_spent = pulp.LpVariable("fuel_spent", lowBound=0, cat='Continuous')

# Objective: Minimize the maximum thrust
problem += fuel_spent

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Model Dynamics and Constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")

problem += (x[T] == x_T, "Target_Position")
problem += (v[T] == v_T, "Target_Velocity")

# Total fuel spent constraint
problem += (fuel_spent == pulp.lpSum([pulp.lpSum([a[t] for t in range(T)])]), "Fuel_Cost")

# Solve the problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[t]) for t in range(1, T+1)]
v_values = [pulp.value(v[t]) for t in range(1, T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent_value = pulp.value(fuel_spent)

# Output Format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent_value,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')