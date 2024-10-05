import pulp
import json

# Data in JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extracting parameters
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)
z = pulp.LpVariable.dicts("z", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(z[i] for i in range(N)), "Total_Illumination_Error"

# Constraints
for i in range(N):
    ill_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # Constraints for z_i
    problem += ill_i - desired_illuminations[i] <= z[i], f"Upper_Bound_Constraint_{i}"
    problem += desired_illuminations[i] - ill_i <= z[i], f"Lower_Bound_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')