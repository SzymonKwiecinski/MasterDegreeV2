import pulp

# Creating the LP problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Variables
x = [pulp.LpVariable(f'x_{t}', cat=pulp.LpContinuous) for t in range(data['T'] + 1)]
v = [pulp.LpVariable(f'v_{t}', cat=pulp.LpContinuous) for t in range(data['T'] + 1)]
a = [pulp.LpVariable(f'a_{t}', cat=pulp.LpContinuous) for t in range(data['T'])]
max_thrust = pulp.LpVariable('max_thrust', lowBound=0, cat=pulp.LpContinuous)

# Objective
problem += max_thrust, "Minimize maximum thrust"

# Initial conditions
problem += (x[0] == data['X0'], "Initial position")
problem += (v[0] == data['V0'], "Initial velocity")

# Constraints for motion equations
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t], f"Position at time {t+1}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity at time {t+1}")

# Target constraints
problem += (x[data['T']] == data['XT'], "Target position")
problem += (v[data['T']] == data['VT'], "Target velocity")

# Constraints on acceleration
for t in range(data['T']):
    problem += (a[t] <= max_thrust, f"Max thrust constraint (positive) at {t}")
    problem += (-a[t] <= max_thrust, f"Max thrust constraint (negative) at {t}")

# Solve the problem
problem.solve()

# Collect the results
result_x = [pulp.value(x[t]) for t in range(data['T'] + 1)]
result_v = [pulp.value(v[t]) for t in range(data['T'] + 1)]
result_a = [pulp.value(a[t]) for t in range(data['T'])]
fuel_spend = sum(abs(pulp.value(a[t])) for t in range(data['T']))

# Output in required format
output = {
    "x": result_x,
    "v": result_v,
    "a": result_a,
    "fuel_spend": fuel_spend
}

print(output)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')