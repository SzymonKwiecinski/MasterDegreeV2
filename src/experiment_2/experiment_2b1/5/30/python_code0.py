import pulp
import json

data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = len(data["y"])

# Create the LP problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Coefficients to be determined
a = pulp.LpVariable("a", cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')
c = pulp.LpVariable("c", cat='Continuous')

# Deviations for each point
deviations = [pulp.LpVariable(f"deviation_{k}", cat='Continuous') for k in range(K)]

# Objective function: minimize sum of deviations
problem += pulp.lpSum(deviations)

# Constraints for each data point
for k in range(K):
    problem += deviations[k] >= data["y"][k] - (c * (data["x"][k] ** 2) + b * data["x"][k] + a)
    problem += deviations[k] >= -(data["y"][k] - (c * (data["x"][k] ** 2) + b * data["x"][k] + a))

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

# Print output and objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')