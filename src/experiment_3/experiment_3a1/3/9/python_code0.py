import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the optimization problem
problem = pulp.LpProblem("RoadIllumination", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)  # power_j >= 0
error = pulp.LpVariable.dicts("Error", range(N), lowBound=0)  # error_i >= 0

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N)), "TotalAbsoluteError"

# Constraints
for i in range(N):
    ill_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += ill_i == desired_illuminations[i], f"IlluminationConstraint_{i+1}"
    
    problem += error[i] >= ill_i - desired_illuminations[i], f"ErrorUpperBound_{i+1}"
    problem += error[i] >= desired_illuminations[i] - ill_i, f"ErrorLowerBound_{i+1}"

# Solve the problem
problem.solve()

# Print the optimal power of each lamp and the objective value
for j in range(M):
    print(f'Power of Lamp {j+1}: {power[j].varValue}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')