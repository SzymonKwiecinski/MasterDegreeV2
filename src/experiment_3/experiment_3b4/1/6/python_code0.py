import pulp

# Data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Problem setup
problem = pulp.LpProblem("Rocket_Control", pulp.LpMinimize)

# Decision variables
T = data['TotalTime']
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
u = [pulp.LpVariable(f"u_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective function
problem += pulp.lpSum(u)

# Constraints
problem += (x[0] == data['InitialPosition'], "Initial_Position")
problem += (v[0] == data['InitialVelocity'], "Initial_Velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Dynamics_Velocity_{t}")
    problem += (u[t] >= a[t], f"Abs_Constraint_Pos_{t}")
    problem += (u[t] >= -a[t], f"Abs_Constraint_Neg_{t}")

problem += (x[T] == data['FinalPosition'], "Final_Position")
problem += (v[T] == data['FinalVelocity'], "Final_Velocity")

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')