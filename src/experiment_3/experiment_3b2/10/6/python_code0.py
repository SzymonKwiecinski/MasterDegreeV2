import pulp

# Data from the JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extracting parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Initialize the problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  # position variables
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  # velocity variables
a_plus = pulp.LpVariable.dicts("a_plus", range(T), lowBound=0)  # acceleration positive part
a_minus = pulp.LpVariable.dicts("a_minus", range(T), lowBound=0)  # acceleration negative part

# Objective Function
problem += pulp.lpSum(a_plus[t] + a_minus[t] for t in range(T))  # minimizing total fuel consumption

# Constraints
problem += (x[0] == x0)  # Initial position constraint
problem += (v[0] == v0)  # Initial velocity constraint

# Dynamics equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  # Position update
    problem += (v[t + 1] == v[t] + a_plus[t] - a_minus[t])  # Velocity update

# Final conditions
problem += (x[T] == xT)  # Final position constraint
problem += (v[T] == vT)  # Final velocity constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')