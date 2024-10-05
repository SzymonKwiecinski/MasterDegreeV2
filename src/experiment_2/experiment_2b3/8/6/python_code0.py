import pulp

# Parsing Data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Problem
problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Objective
problem += pulp.lpSum([pulp.lpSum([a[t]]) for t in range(T)])

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Transition_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Transition_{t}")

# Solve
problem.solve()

# Output Format
output = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective),
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')