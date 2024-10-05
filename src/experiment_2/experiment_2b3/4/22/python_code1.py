import pulp

# Data from the problem
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

K = len(requirement)
I = len(requirement[0])

# Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", 0, recruit_limit[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", 0, num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", 0, num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective: Minimize redundancy costs
redundancy = [
    [pulp.LpVariable(f"redundancy_{k}_{i}", 0, cat='Integer') for i in range(I)]
    for k in range(K)
]
problem += pulp.lpSum(costredundancy[k] * redundancy[k][i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    # Initial manpower involved in calculation
    current_strength = strength[k]

    for i in range(I):
        # Effective manpower available should be equal to or more than the requirement
        problem += (current_strength + recruit[k][i] - redundancy[k][i] + 
                     0.5 * short[k][i] + overmanning[k][i] >= requirement[k][i])

        # Update current strength for next year's calculation (natural wastage)
        if i == 0:
            # First year has higher wastage for new recruits
            next_strength = (current_strength - redundancy[k][i] - 
                             lessonewaste[k] * recruit[k][i]) * (1 - moreonewaste[k])
        else:
            next_strength = (current_strength - redundancy[k][i]) * (1 - moreonewaste[k])
        
        current_strength = next_strength + recruit[k][i]

# Solve the problem
problem.solve()

# Extract results
recruit_result = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_result = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_result = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

# Output
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')