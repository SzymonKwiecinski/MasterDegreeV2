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

# Create problem
problem = pulp.LpProblem("ManpowerPlanning", pulp.LpMinimize)

# Variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=data['recruit'][k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=data['num_overman'], cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=data['num_shortwork'], cat='Integer') for i in range(I)] for k in range(K)]
employed = [[pulp.LpVariable(f"employed_{k}_{i}", lowBound=0, cat='Integer') for i in range(I+1)] for k in range(K)]

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * (employed[k][i] - data['requirement'][k][i]) * (employed[k][i] > data['requirement'][k][i]) +
    data['costoverman'][k] * overmanning[k][i] +
    data['costshort'][k] * short[k][i]
    for k in range(K) for i in range(I)
)

# Constraints

# Initial employment strength
for k in range(K):
    problem += employed[k][0] == data['strength'][k]

# Employment balance
for k in range(K):
    for i in range(1, I+1):
        if i > 1:
            employed_less_1_year = recruit[k][i-1]
            employed_more_1_year = employed[k][i-1] - employed_less_1_year
            employed[k][i] = employed_more_1_year * (1 - data['moreonewaste'][k]) + \
                             employed_less_1_year * (1 - data['lessonewaste'][k]) + \
                             recruit[k][i-1]
        else:
            employed[k][i] = employed[k][0] * (1 - data['moreonewaste'][k]) + recruit[k][0]

# Requirement and manpower balance
for k in range(K):
    for i in range(I):
        manpower_supply = employed[k][i+1] + overmanning[k][i] + short[k][i] * 0.5
        problem += manpower_supply >= data['requirement'][k][i]

# Solve problem
problem.solve()

# Extract solution
solution = {
    "recruit": [[recruit[k][i].varValue for i in range(I)] for k in range(K)],
    "overmanning": [[overmanning[k][i].varValue for i in range(I)] for k in range(K)],
    "short": [[short[k][i].varValue for i in range(I)] for k in range(K)]
}

# Output
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')