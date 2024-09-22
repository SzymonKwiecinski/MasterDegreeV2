import pulp

# Data Inputs
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

# Unpacking the data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)  # number of categories of manpower
I = len(requirement[0])  # number of years

# Problem
problem = pulp.LpProblem("Manpower Planning", pulp.LpMinimize)

# Decision Variables
recruit_vars = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=recruit[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning_vars = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective Function
problem += pulp.lpSum([costredundancy[k] * (strength[k] + 
                                            sum(recruit_vars[k][0:i]) - 
                                            sum(requirement[k][0:i]) - 
                                            sum(short_vars[k][0:i]) +
                                            sum(overmanning_vars[k][0:i]))
                        for k in range(K) for i in range(I)])

# Constraints

# Workforce balance constraints
for k in range(K):
    workforce = strength[k]
    for i in range(I):
        problem += (workforce + recruit_vars[k][i] + overmanning_vars[k][i] + 0.5 * short_vars[k][i] >= requirement[k][i])
        workforce = (workforce + recruit_vars[k][i] - 
                     lessonewaste[k] * recruit_vars[k][i] - 
                     moreonewaste[k] * (workforce - recruit_vars[k][i]))

# Solving the Problem
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')