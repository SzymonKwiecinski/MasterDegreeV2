import pulp

# Data provided
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Extracting data
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Define the linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Calculate illumination for segment i
    ill_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # Error constraints
    problem += error[i] >= ill_i - desired_illuminations[i], f"Error_Upper_{i}"
    problem += error[i] >= desired_illuminations[i] - ill_i, f"Error_Lower_{i}"

# Solve the problem
problem.solve()

# Output the results
for j in range(M):
    print(f"Optimal power of lamp {j+1}: {power[j].varValue}")

total_error = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')