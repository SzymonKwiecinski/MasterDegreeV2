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

# Extract data from json
requirements = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_capacity = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Constants
K = len(requirements)
I = len(requirements[0])

# Problem
problem = pulp.LpProblem("ManpowerPlanning", pulp.LpMinimize)

# Variables
recruit_vars = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]
overmanning_vars = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=num_overman, cat='Continuous') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=num_shortwork, cat='Continuous') for i in range(I)] for k in range(K)]

# Objective Function
cost = pulp.lpSum([
    costredundancy[k] * (strength[k] - recruit_vars[k][0] * (1 - lessonewaste[k]) - requirements[k][0] + short_vars[k][0] / 2 + overmanning_vars[k][0])
    + pulp.lpSum([
        (costredundancy[k] * (recruit_vars[k][i-1] * (1 - lessonewaste[k]) * (1 - moreonewaste[k])) +
        costoverman[k] * overmanning_vars[k][i] +
        costshort[k] * short_vars[k][i])
        for i in range(1, I)
    ])
    for k in range(K)
])

problem += cost

# Constraints
for k in range(K):
    # Initial year
    problem += strength[k] + recruit_vars[k][0] * (1 - lessonewaste[k]) == requirements[k][0] - short_vars[k][0] / 2 + overmanning_vars[k][0]
    for i in range(1, I):
        problem += (
            recruit_vars[k][i-1] * (1 - lessonewaste[k]) * (1 - moreonewaste[k])
            + recruit_vars[k][i]
            == requirements[k][i] - short_vars[k][i] / 2 + overmanning_vars[k][i]
        )
    # Recruitment limit
    for i in range(I):
        problem += recruit_vars[k][i] <= recruit_capacity[k]

# Solve
problem.solve()

# Results
results = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')