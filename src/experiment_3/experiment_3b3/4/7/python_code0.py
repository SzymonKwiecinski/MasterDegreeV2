import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0, V0, XT, VT, T = data['X0'], data['V0'], data['XT'], data['VT'], data['T']

# Create a Linear Programming Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", (range(T)), lowBound=None, upBound=None, cat='Continuous')
x = pulp.LpVariable.dicts("x", (range(T + 1)), lowBound=None, upBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", (range(T + 1)), lowBound=None, upBound=None, cat='Continuous')

# Auxiliary Variable for Objective Function
max_abs_a = pulp.LpVariable("max_abs_a", lowBound=0, cat='Continuous')

# Objective Function: Minimize the maximum acceleration magnitude
problem += max_abs_a, "Minimize_Max_Acceleration"

# Constraints

# Initial conditions
problem += x[0] == X0, "Initial_Position"
problem += v[0] == V0, "Initial_Velocity"

# Dynamical model
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Equation_at_t_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Equation_at_t_{t}"

    # Maximum acceleration constraint
    problem += a[t] <= max_abs_a, f"Max_Acceleration_Positive_at_t_{t}"
    problem += -a[t] <= max_abs_a, f"Max_Acceleration_Negative_at_t_{t}"

# Terminal conditions
problem += x[T] == XT, "Final_Position"
problem += v[T] == VT, "Final_Velocity"

# Solve the problem
problem.solve()

# Extracting the results
x_values = [x[t].varValue for t in range(T + 1)]
v_values = [v[t].varValue for t in range(T + 1)]
a_values = [a[t].varValue for t in range(T)]

# Assuming fuel spend is the sum of absolute accelerations
fuel_spend = sum(abs(at) for at in a_values)

# Output
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spend
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')