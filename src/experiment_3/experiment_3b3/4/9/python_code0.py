import pulp

# Data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Illumination_Optimization", pulp.LpMinimize)

# Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0, cat=pulp.LpContinuous)
illumination = pulp.LpVariable.dicts("illumination", range(N), cat=pulp.LpContinuous)
absolute_error = pulp.LpVariable.dicts("absolute_error", range(N), lowBound=0, cat=pulp.LpContinuous)

# Objective
problem += pulp.lpSum(absolute_error[i] for i in range(N))

# Constraints
for i in range(N):
    problem += illumination[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += absolute_error[i] >= illumination[i] - desired_illuminations[i]
    problem += absolute_error[i] >= desired_illuminations[i] - illumination[i]

# Solve
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output power settings for each lamp
for j in range(M):
    print(f'Power of lamp {j}: {pulp.value(power[j])}')

# Total absolute error
total_error = sum(pulp.value(absolute_error[i]) for i in range(N))
print(f'Total absolute error: {total_error}')