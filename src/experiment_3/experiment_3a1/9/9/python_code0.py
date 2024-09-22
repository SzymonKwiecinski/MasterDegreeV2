import pulp

# Given data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables: power_j for j in 1 to M
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Auxiliary variables for absolute errors
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective: minimize the total error
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints for each segment illumination
for i in range(N):
    # The illumination for segment i
    illumination = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    
    # Constraint for the absolute error
    problem += illumination - desired[i] <= error[i], f"Upper_Error_Constraint_{i}"
    problem += - (illumination - desired[i]) <= error[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the results
for j in range(M):
    print(f'Optimal power for lamp {j + 1}: {power[j].varValue}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')