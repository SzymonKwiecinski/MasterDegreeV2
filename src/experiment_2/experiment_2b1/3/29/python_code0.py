import json
import pulp

# Input data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Define the problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable("intercept", lowBound=None)  # Intercept
b = pulp.LpVariable("slope", lowBound=None)      # Slope
deviation = pulp.LpVariable.dicts("deviation", range(data['NumObs']), lowBound=0)

# Objective function: Minimize the maximum deviation
problem += pulp.lpSum([deviation[k] for k in range(data['NumObs'])]), "Minimize_Max_Deviation"

# Constraints: y_k - (b * x_k + a) <= deviation_k for each k
for k in range(data['NumObs']):
    problem += data['Y'][k] - (b * data['X'][k] + a) <= deviation[k], f"Upper_Bound_Constraint_{k}"
    problem += -(data['Y'][k] - (b * data['X'][k] + a)) <= deviation[k], f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue

print(json.dumps({"intercept": intercept, "slope": slope}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')