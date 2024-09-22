import pulp
import json

# Given data
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define the decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=0)          # Acceleration (non-negative)

# Initial Conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Final Conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Objective Function: Minimize total fuel consumption (acceleration)
problem += pulp.lpSum(a[t] for t in range(T))

# Motion Constraints
for t in range(T):
    problem += x[t + 1] - x[t] == v[t]  # Position
    problem += v[t + 1] - v[t] == a[t]  # Velocity

# Solve the problem
problem.solve()

# Retrieve the results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')