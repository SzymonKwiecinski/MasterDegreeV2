import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extracting data
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("RocketThrustOptimization", pulp.LpMinimize)

# Decision variables for acceleration
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Decision variables for position and velocity
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)

# Objective: Minimize the maximum absolute thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints for position and velocity state equations
problem += x[0] == x0
problem += v[0] == v0

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
  
# Constraints for the final position and final velocity
problem += x[T] == xT
problem += v[T] == vT

# Constraints for thrust limits
for t in range(T):
    problem += a[t] <= max_thrust
    problem += a[t] >= -max_thrust

# Solve the problem
problem.solve()

# Collecting results
x_values = [x[i].varValue for i in range(T + 1)]
v_values = [v[i].varValue for i in range(T + 1)]
a_values = [a[i].varValue for i in range(T)]
fuel_spent = sum(abs(a[i].varValue) for i in range(T))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spent": fuel_spent,
}

# To view the output
print(output)