import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration at each time step
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position at each time step
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity at each time step
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)

# Objective function: minimize the maximum thrust required
problem += max_thrust

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Constraints for the dynamics of the rocket
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += max_thrust >= a[t]  # max thrust constraint
    problem += max_thrust >= -a[t]  # max thrust constraint for negative acceleration

# Final position and velocity conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Solve the problem
problem.solve()

# Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Output results
output = {
    "x": positions[1:],  # excluding x_0
    "v": velocities[1:],  # excluding v_0
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')