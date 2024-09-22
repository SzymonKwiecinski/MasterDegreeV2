import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a problem variable
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
max_a = pulp.LpVariable("max_a", lowBound=0)

# Objective Function: Minimize the maximum thrust required
problem += max_a, "Minimize Maximum Thrust"

# Constraints
problem += x[0] == x_0, "Initial Position"
problem += v[0] == v_0, "Initial Velocity"
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= max_a, f"Max_Thrust_Upper_Bound_{t}"
    problem += -a[t] <= max_a, f"Max_Thrust_Lower_Bound_{t}"

# Final constraints
problem += x[T] == x_T, "Final Position"
problem += v[T] == v_T, "Final Velocity"

# Solve the problem
problem.solve()

# Prepare Output
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a) * T  # total fuel spent is max_a * T since accelerations are assumed constant

# Output Result
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')