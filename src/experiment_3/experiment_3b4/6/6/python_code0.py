import pulp

# Extracting data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the Linear Programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", (range(T)), lowBound=None, cat='Continuous')
x = pulp.LpVariable.dicts("x", (range(T+1)), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", (range(T+1)), lowBound=None, cat='Continuous')
u = pulp.LpVariable.dicts("u", (range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(u[t] for t in range(T)), "Minimize fuel consumption"

# Constraints
# Initial Conditions
problem += (x[0] == x_0), "Initial_Position"
problem += (v[0] == v_0), "Initial_Velocity"

# Final Conditions
problem += (x[T] == x_T), "Final_Position"
problem += (v[T] == v_T), "Final_Velocity"

# System Dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Equation_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Equation_{t}"

# Fuel Consumption Constraints
for t in range(T):
    problem += (a[t] <= u[t]), f"Positive_Acceleration_Constraint_{t}"
    problem += (-a[t] <= u[t]), f"Negative_Acceleration_Constraint_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')