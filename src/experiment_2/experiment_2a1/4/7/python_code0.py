import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Variables
T = data['T']
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-pulp.LpInfinity, upBound=pulp.LpInfinity) for t in range(T)]

# Objective: Minimize max_t |a_t|
max_a = pulp.LpVariable('max_a', lowBound=0)
problem += max_a

# Constraints
problem += x[0] == x0
problem += v[0] == v0

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_a
    problem += a[t] >= -max_a

# Final conditions
problem += x[T] == xT
problem += v[T] == vT

# Solve the problem
problem.solve()

# Extract results
x_results = [pulp.value(x[t]) for t in range(T + 1)]
v_results = [pulp.value(v[t]) for t in range(T + 1)]
a_results = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a)

# Prepare output
output = {
    "x": x_results,
    "v": v_results,
    "a": a_results,
    "fuel_spend": fuel_spent,
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')