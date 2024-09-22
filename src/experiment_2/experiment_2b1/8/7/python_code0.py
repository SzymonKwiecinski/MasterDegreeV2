import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a LP problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Create decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Define the initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Define the equations based on the model
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Define final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Objective: minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
for t in range(T):
    problem += (a[t] <= max_thrust, f"Thrust_Uppper_Bound_{t}")
    problem += (a[t] >= -max_thrust, f"Thrust_Lower_Bound_{t}")

problem += max_thrust, "Minimize_Max_Thrust"

# Solve the problem
problem.solve()

# Prepare the output
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust)

# Output the results
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')