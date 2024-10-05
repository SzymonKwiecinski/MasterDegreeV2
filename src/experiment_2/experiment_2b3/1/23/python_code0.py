import pulp

# Data input
data = {
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    "strength": [2000, 1500, 1000],
    "lessonewaste": [0.25, 0.2, 0.1],
    "moreonewaste": [0.1, 0.05, 0.05],
    "recruit": [500, 800, 500],
    "costredundancy": [200, 500, 500],
    "num_overman": 150,
    "costoverman": [1500, 2000, 3000],
    "num_shortwork": 50,
    "costshort": [500, 400, 400]
}

requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limits = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)  # number of manpower types
I = len(requirement[0])  # number of years

# Initialize the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, upBound=recruit_limits[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f'overman_{k}_{i}', lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function
problem += pulp.lpSum(
    recruit[k][i] * costredundancy[k] +
    overmanning[k][i] * costoverman[k] +
    short[k][i] * costshort[k]
    for k in range(K) for i in range(I)
)

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            manpower_available = strength[k]
        else:
            previous_year_manpower = (manpower_available - recruit[k][i-1] * lessonewaste[k]) * (1 - moreonewaste[k])
            manpower_available = previous_year_manpower + recruit[k][i-1]

        problem += (manpower_available + recruit[k][i] + overmanning[k][i] + 0.5 * short[k][i] >= requirement[k][i]), f'Constraint_{k}_{i}_supply'

# Solve the problem
problem.solve()

# Output the results
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')