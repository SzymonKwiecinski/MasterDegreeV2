import pulp

# Data input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Variables
NumObs = data["NumObs"]
Y = data["Y"]
X = data["X"]

# Create the LP problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
d = pulp.LpVariable("max_deviation", lowBound=0)

# Objective function
problem += d

# Constraints for minimizing the maximum deviation
for k in range(NumObs):
    problem += Y[k] - (b * X[k] + a) <= d
    problem += (b * X[k] + a) - Y[k] <= d

# Solve the problem
problem.solve()

# Extracting results
intercept = a.varValue
slope = b.varValue

# Output
output = {
    "intercept": intercept,
    "slope": slope
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
print(output)