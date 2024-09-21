import pulp

# Data from JSON
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

# Unpacking data
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables
P = [pulp.LpVariable(f'P_{j}', lowBound=0) for j in range(M)]
E = [pulp.LpVariable(f'E_{i}', lowBound=0) for i in range(N)]

# Objective Function
problem += pulp.lpSum(E[i] for i in range(N))

# Constraints
for i in range(N):
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i]), f"Constraint1_{i}"
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i]), f"Constraint2_{i}"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')