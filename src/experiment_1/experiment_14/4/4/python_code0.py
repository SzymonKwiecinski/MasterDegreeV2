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

# Unpack data
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision variables
P = [pulp.LpVariable(f'P_{j}', lowBound=0) for j in range(M)]
E = [pulp.LpVariable(f'E_{i}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum(E[i] for i in range(N)), "Total Absolute Error"

# Constraints
for i in range(N):
    problem += pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i], f"Upper_Error_Constraint_{i}"
    problem += DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optionally, print the values of the decision variables
for j in range(M):
    print(f'P_{j} = {pulp.value(P[j])}')

for i in range(N):
    print(f'E_{i} = {pulp.value(E[i])}')