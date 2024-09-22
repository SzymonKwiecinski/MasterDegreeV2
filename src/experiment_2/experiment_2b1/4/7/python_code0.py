import pulp
import json

data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extract data from the input
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Max_Thrust", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position at each time step
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity at each time step
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       # acceleration at each time step

# Set the initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Add the constraints for position and velocity
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Ensure the final conditions are met
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective: minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust")
for t in range(T):
    problem += (a[t] <= max_thrust)
    problem += (a[t] >= -max_thrust)

problem += max_thrust  # Objective function

# Solve the problem
problem.solve()

# Retrieve the results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust) * T  # Total fuel spent calculation

# Prepare the output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')