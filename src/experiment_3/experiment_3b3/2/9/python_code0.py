import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [
        [0.5, 0.3],
        [0.2, 0.4],
        [0.1, 0.6]
    ],
    'DesiredIlluminations': [14, 3, 12]
}

# Parameters
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables
power = [pulp.LpVariable(f'power_{j+1}', lowBound=0) for j in range(M)]
error = [pulp.LpVariable(f'error_{i+1}', lowBound=0) for i in range(N)]

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += illumination - error[i] <= desired_illuminations[i], f"Illumination_Constraint_1_Segment_{i+1}"
    problem += -illumination + error[i] <= desired_illuminations[i], f"Illumination_Constraint_2_Segment_{i+1}"

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optimal powers
for j in range(M):
    print(f"Optimal power for lamp {j+1}: {pulp.value(power[j])}")