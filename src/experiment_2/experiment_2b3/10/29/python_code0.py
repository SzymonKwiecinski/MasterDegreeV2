import pulp

# Data from JSON
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract data
Y = data['Y']
X = data['X']
NumObs = data['NumObs']

# Define the problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')  # Intercept
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')  # Slope
z = pulp.LpVariable('z', lowBound=0, upBound=None, cat='Continuous')     # Maximum deviation

# Objective: Minimize the maximum deviation (z)
problem += z, "Objective is to minimize the maximum deviation"

# Add constraints to ensure absolute deviations are captured
for i in range(NumObs):
    yi = Y[i]
    xi = X[i]
    problem += yi - (b * xi + a) <= z, f"Deviation_positive_{i}"
    problem += (b * xi + a) - yi <= z, f"Deviation_negative_{i}"

# Solve the problem
problem.solve()

# Extract results
intercept = pulp.value(a)
slope = pulp.value(b)

# Prepare output
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')