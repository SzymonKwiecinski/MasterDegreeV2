import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extracting input values
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Fuel_Optimization", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration at time t
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position at time t
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity at time t

# Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Final conditions
problem += (x[T] == xT)
problem += (v[T] == vT)

# Objective: minimize the maximum thrust required
max_a = pulp.LpVariable("max_a", lowBound=0)
for t in range(T):
    problem += (a[t] <= max_a)
    problem += (-a[t] <= max_a)

problem += max_a

# Solve the problem
problem.solve()

# Prepare the result
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a)

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')