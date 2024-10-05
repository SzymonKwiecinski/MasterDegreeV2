import pulp

# Input data
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

# Parameters
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Decision variables
K = len(requirement)  # number of manpower categories
I = len(requirement[0])  # number of years

# Defining problem
problem = pulp.LpProblem("Minimum_Redundancy_Problem", pulp.LpMinimize)

# Create decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=recruit_limit[0], cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=num_overman, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=num_shortwork, cat='Integer')

# Objective function: Minimize redundancy
problem += pulp.lpSum([costredundancy[k] * (strength[k] + 
            sum(recruit[k][j] * (1-lessonewaste[k])**(j+1) for j in range(i)) - requirement[k][i]) 
            for k in range(K) for i in range(I)]), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            effective_strength = strength[k]
        else:
            effective_strength = strength[k] * (1 - moreonewaste[k]) + sum(recruit[k][j] * (1 - lessonewaste[k])**(i-j) for j in range(i))

        # Manpower requirement constraint
        problem += effective_strength + recruit[k][i] + overmanning[k][i] + short[k][i] * 0.5 >= requirement[k][i]

        # Redundancy should not exceed the overmanning capability
        problem += effective_strength + recruit[k][i] - requirement[k][i] <= overmanning[k][i]

# Solve the problem
problem.solve()

# Gather results
recruit_res = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_res = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_res = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_res,
    "overmanning": overmanning_res,
    "short": short_res
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')