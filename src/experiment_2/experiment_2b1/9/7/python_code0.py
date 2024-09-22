import pulp

# Data from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize the maximum thrust (maximum acceleration)
max_a = pulp.LpVariable('max_a', lowBound=0)
problem += max_a

# Constraints
problem += (x[0] == x_0, "Initial Position")
problem += (v[0] == v_0, "Initial Velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (a[t] <= max_a, f"Max_Thrust_Constraint_{t}")
    problem += (a[t] >= -max_a, f"Min_Thrust_Constraint_{t}")

problem += (x[T] == x_T, "Final_Position_Constraint")
problem += (v[T] == v_T, "Final_Velocity_Constraint")

# Solve the problem
problem.solve()

# Collect results
result_x = [pulp.value(x[t]) for t in range(T + 1)]
result_v = [pulp.value(v[t]) for t in range(T + 1)]
result_a = [pulp.value(a[t]) for t in range(T)]

fuel_spent = pulp.value(max_a) * T  # Total fuel spent is max acceleration * time

# Output results
output = {
    "x": result_x,
    "v": result_v,
    "a": result_a,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')