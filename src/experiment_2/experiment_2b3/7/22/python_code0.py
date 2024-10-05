import pulp

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

# Extract data from the input
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

num_years = len(requirement[0])
num_categories = len(strength)

# Define the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Integer')

# Objective: Minimize redundancy
problem += pulp.lpSum(costredundancy[k] * (strength[k] + 
                                           pulp.lpSum(recruit_vars[(k, j)] for j in range(i)) -
                                           requirement[k][i] -
                                           overmanning_vars[(k, i)] -
                                           0.5 * short_vars[(k, i)])
                      for k in range(num_categories) for i in range(num_years))

# Constraints
for k in range(num_categories):
    for i in range(num_years):
        # Recruit limit constraint
        problem += recruit_vars[(k, i)] <= recruit[k]
        
        # Overmanning constraint
        problem += pulp.lpSum(overmanning_vars[(k, j)] for k in range(num_categories) for j in range(num_years)) <= num_overman
        
        # Short-time working constraint
        problem += short_vars[(k, i)] <= num_shortwork

        current_strength = strength[k] + pulp.lpSum(recruit_vars[(k, j)] for j in range(i))
        # Total manpower meets the requirement
        problem += current_strength - requirement[k][i] >= 0

# Solve the problem
problem.solve()

# Extract results
result_recruit = [[pulp.value(recruit_vars[(k, i)]) for i in range(num_years)] for k in range(num_categories)]
result_overmanning = [[pulp.value(overmanning_vars[(k, i)]) for i in range(num_years)] for k in range(num_categories)]
result_short = [[pulp.value(short_vars[(k, i)]) for i in range(num_years)] for k in range(num_categories)]

# Results
output = {
    "recruit": result_recruit,
    "overmanning": result_overmanning,
    "short": result_short
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')