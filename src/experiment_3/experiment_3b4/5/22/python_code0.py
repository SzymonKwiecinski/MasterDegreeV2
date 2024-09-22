import pulp

# Data
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

K = len(data['strength'])
I = len(data['requirement'][0])

# Decision Variables
R = pulp.LpVariable.dicts("Recruits", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
O = pulp.LpVariable.dicts("Overmanning", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("ShortTime", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
X = pulp.LpVariable.dicts("LessThanOneYear", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
Y = pulp.LpVariable.dicts("MoreThanOneYear", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - (Y[k, i] + O[k, i] - S[k, i]))
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(1, I):
        # Strength Balance
        problem += Y[k, i] == (1 - data['moreonewaste'][k]) * Y[k, i-1] + (1 - data['lessonewaste'][k]) * X[k, i-1] + R[k, i-1]
        problem += X[k, i] == R[k, i-1]

    # Initial condition
    problem += Y[k, 0] == data['strength'][k]

    for i in range(I):
        # Manpower Requirement
        problem += Y[k, i] + 0.5 * S[k, i] + O[k, i] >= data['requirement'][k][i]

        # Short-time Work Limit
        problem += S[k, i] <= data['num_shortwork']

        # Recruitment Limit
        problem += R[k, i] <= data['recruit'][k]

for i in range(I):
    # Overmanning Limit
    problem += pulp.lpSum(O[k, i] for k in range(K)) <= data['num_overman']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')