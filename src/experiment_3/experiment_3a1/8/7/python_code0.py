import pulp
import json

# Given data in JSON format
data = '{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}'
parameters = json.loads(data)

# Assign parameters
x0 = parameters['X0']
v0 = parameters['V0']
xT = parameters['XT']
vT = parameters['VT']
T = parameters['T']

# Define the problem
problem = pulp.LpProblem("Rocket_Movement_Problem", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

# Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Final state constraints
problem += (x[T] == xT)
problem += (v[T] == vT)

# Max thrust limit
A = pulp.LpVariable("A", lowBound=0)  # Thrust limit
for t in range(T):
    problem += (a[t] <= A)
    problem += (a[t] >= -A)

# Objective function: minimize the maximum thrust requirement
problem += (A)

# Solve the problem
problem.solve()

# Collect results
results = {
    "x": [pulp.value(x[i]) for i in range(T+1)],
    "v": [pulp.value(v[i]) for i in range(T+1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')