import pulp
import json

# Data provided in JSON format
data = json.loads("{'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}")

# Extracting parameters from data
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Decision variables for lamp power
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Auxiliary variables for absolute error
e = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: minimize sum of errors
problem += pulp.lpSum(e[i] for i in range(N))

# Constraints for each segment
for i in range(N):
    ill_i = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += ill_i - desired[i] <= e[i]
    problem += desired[i] - ill_i <= e[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')