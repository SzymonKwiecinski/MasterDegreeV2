import pulp
import json

# Load data from the provided JSON
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')

# Extract parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat=pulp.LpContinuous)
v = pulp.LpVariable.dicts("v", range(T+1), cat=pulp.LpContinuous)
a = pulp.LpVariable.dicts("a", range(T), cat=pulp.LpContinuous)

# Define absolute value variables for acceleration
u = pulp.LpVariable.dicts("u", range(T), lowBound=0)

# Objective function: Minimize the total fuel consumption
problem += pulp.lpSum(u[t] for t in range(T)), "Objective"

# Initial conditions
problem += (x[0] == x0), "Initial_Position"
problem += (v[0] == v0), "Initial_Velocity"

# Final conditions
problem += (x[T] == xT), "Final_Position"
problem += (v[T] == vT), "Final_Velocity"

# Evolution equations for position and velocity
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Update_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Update_{t}"

# Absolute value constraints for acceleration
for t in range(T):
    problem += (a[t] <= u[t]), f"Abs_Constr_Pos_{t}"
    problem += (-a[t] <= u[t]), f"Abs_Constr_Neg_{t}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')