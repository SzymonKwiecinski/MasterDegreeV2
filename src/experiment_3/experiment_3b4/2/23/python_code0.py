import pulp

# Define the data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

# Indices
K = len(data['strength'])
I = len(data['requirement'][0])

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
R = pulp.LpVariable.dicts("Recruitment", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')
O = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')
S = pulp.LpVariable.dicts("Shortwork", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * R[k][i] + data['costoverman'][k] * O[k][i] + data['costshort'][k] * S[k][i]
                      for k in range(K) for i in range(I))

# Constraints
# 1. Manpower Balance Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) - (data['strength'][k] * data['lessonewaste'][k]) 
            + R[k][i] - O[k][i] - 0.5 * S[k][i] == data['requirement'][k][i]
        )

# 2. Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += R[k][i] <= data['recruit'][k]

# 3. Overmanning Limits
for i in range(I):
    problem += pulp.lpSum(O[k][i] for k in range(K)) <= data['num_overman']

# 4. Short-time Work Limits
for k in range(K):
    for i in range(I):
        problem += S[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')