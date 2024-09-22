import pulp
import json

# Load data from JSON format
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Constraints
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionConstraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityConstraint_{t}"

problem += x[T] == x_T, "FinalPositionConstraint"
problem += v[T] == v_T, "FinalVelocityConstraint"

# Objective function
problem += pulp.lpSum(pulp.lpAbs(a[t]) for t in range(T)), "FuelConsumption"

# Solve the problem
problem.solve()

# Collecting results
positions = [x[i].varValue for i in range(T + 1)]
velocities = [v[i].varValue for i in range(T + 1)]
accelerations = [a[i].varValue for i in range(T)]

# Output results
fuel_spent = pulp.value(problem.objective)

output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent
}

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')