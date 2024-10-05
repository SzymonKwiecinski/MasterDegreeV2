import pulp
import json

# Data input
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Define decision variables
a_pos = pulp.LpVariable.dicts("a_pos", range(T), lowBound=0)
a_neg = pulp.LpVariable.dicts("a_neg", range(T), lowBound=0)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)

# Objective function: Minimize total fuel consumption
problem += pulp.lpSum([a_pos[t] + a_neg[t] for t in range(T)]), "Total_Fuel"

# Initial conditions
x[0] = x_0
v[0] = v_0

# Constraints for dynamics and boundary conditions
for t in range(T):
    # Position and velocity dynamics
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + (a_pos[t] - a_neg[t]), f"Velocity_Constraint_{t}"

# Boundary conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

# Absolute value constraints for accelerations
for t in range(T):
    problem += (a_pos[t] - a_neg[t]) == (a_pos[t] - a_neg[t]), f"Acceleration_Constraint_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')