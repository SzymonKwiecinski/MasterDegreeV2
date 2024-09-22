import pulp

# Data extracted from the <DATA> tag
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

K = len(data['strength'])    # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("r", (range(K), range(I)), lowBound=0, cat='Continuous')  # Recruits
o = pulp.LpVariable.dicts("o", (range(K), range(I)), lowBound=0, cat='Continuous')  # Overmanned employees
s = pulp.LpVariable.dicts("s", (range(K), range(I)), lowBound=0, cat='Continuous')  # Short-time working employees

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * pulp.lpSum(pulp.max(0, o[k][i] - data['requirement'][k][i]) for i in range(I)) for k in range(K))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower Requirement Constraint
        problem += (data['strength'][k] - pulp.lpSum(r[k][j] + s[k][j] for j in range(i + 1)) + 
                    data['strength'][k] * data['moreonewaste'][k] * (i + 1) >= 
                    data['requirement'][k][i] - o[k][i])

        # Recruitment Limit
        problem += r[k][i] <= data['recruit'][k]

        # Overmanning Limit
        problem += o[k][i] <= data['num_overman']

        # Short-time Working Limit
        problem += s[k][i] <= data['num_shortwork']

        # Short-time Equivalent
        problem += (s[k][i] / 2 + data['strength'][k] - 
                    data['strength'][k] * data['moreonewaste'][k] * (i + 1) >= 
                    data['requirement'][k][i] - o[k][i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')