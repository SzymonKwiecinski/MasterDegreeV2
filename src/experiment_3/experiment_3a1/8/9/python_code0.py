import pulp
import json

# Data provided in JSON format
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')

# Extract parameters from the data
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("Road_Illumination_Optimization", pulp.LpMinimize)

# Decision variables for the powers of the lamps
power_vars = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Auxiliary variables for absolute error
e_vars = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Add the objective function to minimize the total absolute error
problem += pulp.lpSum(e_vars[i] for i in range(N))

# Constraints for each segment of the road
for i in range(N):
    # Illumination for segment i
    illumination_expr = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    
    # Constraints for the auxiliary variables
    problem += e_vars[i] >= illumination_expr - desired_illuminations[i]
    problem += e_vars[i] >= desired_illuminations[i] - illumination_expr

# Solve the problem
problem.solve()

# Print the results
for j in range(M):
    print(f'Power of lamp {j + 1}: {power_vars[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')