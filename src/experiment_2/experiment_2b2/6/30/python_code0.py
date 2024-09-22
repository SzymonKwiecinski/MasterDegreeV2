from pulp import LpProblem, LpVariable, lpSum, LpMinimize
import pulp
import json

# Read the data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y = data['y']
x = data['x']
n = len(y)

# Create the LP problem
problem = LpProblem("Quadratic_Fit", LpMinimize)

# Create variables
a = LpVariable('a', lowBound=-1000, upBound=1000)
b = LpVariable('b', lowBound=-1000, upBound=1000)
c = LpVariable('c', lowBound=-1000, upBound=1000)
deviations = LpVariable.dicts("deviation", range(n), lowBound=0)

# Objective function
problem += lpSum(deviations[i] for i in range(n)), "Minimize_Sum_of_Absolute_Deviations"

# Add constraints
for i in range(n):
    quadratic_expr = c * x[i]**2 + b * x[i] + a
    problem += quadratic_expr - y[i] <= deviations[i], f"Constraint_Pos_{i}"
    problem += -quadratic_expr + y[i] <= deviations[i], f"Constraint_Neg_{i}"

# Solve the problem
problem.solve()

# Get results
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Prepare output
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')