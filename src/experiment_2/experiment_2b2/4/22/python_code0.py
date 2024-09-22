import pulp

# Data
data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}

requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshortwork = data['costshort']

K = len(strength)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f'overmanning_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]
redundancy = [[pulp.LpVariable(f'redundancy_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimize redundancy cost
problem += pulp.lpSum(costredundancy[k] * redundancy[k][i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    available = strength[k]
    for i in range(I):
        # Requirement constraints considering wastage
        problem += (available + recruit[k][i] - redundancy[k][i] - 0.5 * short[k][i] + overmanning[k][i] >= requirement[k][i])
        # Update available workers for next year
        if i != I - 1:
            available = (available + recruit[k][i]) * (1 - lessonewaste[k]) - redundancy[k][i] - 0.5 * short[k][i] + overmanning[k][i]
            available *= (1 - moreonewaste[k])

        # Recruitment limit
        problem += (recruit[k][i] <= recruit_limit[k])
        # Overmanning constraints
        problem += (pulp.lpSum(overmanning[k][i] for k in range(K)) <= num_overman)
        # Short-time working constraints
        problem += (short[k][i] <= num_shortwork)

# Solve the problem
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')