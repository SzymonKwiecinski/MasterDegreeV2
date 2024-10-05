import pulp

# Parse the data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Define parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem('RocketOptimization', pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None, upBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, upBound=None, cat='Continuous')
u = pulp.LpVariable.dicts("u", range(T), lowBound=0, upBound=None, cat='Continuous')  # Auxiliary variables for |a_t|

# Objective function: Minimize the total fuel consumption
problem += pulp.lpSum(u[t] for t in range(T))

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Dynamics_Velocity_{t}")

# Boundary conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Constraints for absolute value representation
for t in range(T):
    problem += (a[t] <= u[t], f"Abs_Constraint_Pos_{t}")
    problem += (-a[t] <= u[t], f"Abs_Constraint_Neg_{t}")

# Solve the problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]

# Calculate total fuel spent
fuel_spent = pulp.value(problem.objective)

# Print the results
print(f"x: {x_values}")
print(f"v: {v_values}")
print(f"a: {a_values}")
print(f"fuel_spend: {fuel_spent}")

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')