from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Parameters
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Model
problem = LpProblem("Rocket_Trajectory_Optimization", LpMinimize)

# Variables
x = [LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [LpVariable(f'a_{t}', lowBound=None, cat='Continuous') for t in range(T)]

# Auxiliary variable for max |a_t|
max_a = LpVariable('max_a', lowBound=0, cat='Continuous')

# Objective
problem += max_a

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Equation_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Equation_{t}")
    problem += (a[t] <= max_a, f"Max_Acc_Constraint_Pos_{t}")
    problem += (-a[t] <= max_a, f"Max_Acc_Constraint_Neg_{t}")

problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Solve the problem
problem.solve()

# Prepare the output
x_values = [value(x[t]) for t in range(1, T+1)]
v_values = [value(v[t]) for t in range(1, T+1)]
a_values = [value(a[t]) for t in range(T)]
fuel_spent = sum(abs(value(a[t])) for t in range(T))

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f'(Objective Value): <OBJ>{value(problem.objective)}</OBJ>')