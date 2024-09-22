import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Extracting data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Control_Problem", pulp.LpMinimize)

# Define the variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
u = [pulp.LpVariable(f'u_{t}', lowBound=0) for t in range(T)]

# Objective function
problem += pulp.lpSum(u[t] for t in range(T)), "Total_Fuel_Consumption"

# Initial conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

# Final conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Motion equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Eq_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Eq_{t}"

# Absolute value constraints
for t in range(T):
    problem += u[t] >= a[t], f"Absolute_Value_Constraint_Pos_{t}"
    problem += u[t] >= -a[t], f"Absolute_Value_Constraint_Neg_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')