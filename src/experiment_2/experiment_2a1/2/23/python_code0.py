import pulp
import json

# Data input
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

requirements = data['requirement']
num_years = len(requirements[0])
num_skills = len(requirements)

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(num_skills), range(num_years)), 0, None, pulp.LpInteger)
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(num_skills), range(num_years)), 0, None, pulp.LpInteger)
short_vars = pulp.LpVariable.dicts("short", (range(num_skills), range(num_years)), 0, None, pulp.LpInteger)

# Objective function: Minimize costs
cost_function = pulp.lpSum(recruit_vars[k][i] * data['costredundancy'][k] for k in range(num_skills) for i in range(num_years)) + \
                   pulp.lpSum(overmanning_vars[k][i] * data['costoverman'][k] for k in range(num_skills) for i in range(num_years)) + \
                   pulp.lpSum(short_vars[k][i] * data['costshort'][k] for k in range(num_skills) for i in range(num_years))

problem += cost_function

# Constraints
for i in range(num_years):
    for k in range(num_skills):
        # Ensure requirements are met
        problem += (data['strength'][k] * (1 - data['moreonewaste'][k]) + \
                     pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) - \
                     pulp.lpSum(overmanning_vars[k][j] for j in range(i + 1)) + \
                     pulp.lpSum(short_vars[k][j] for j in range(i + 1)) >= requirements[k][i]

# Recruitment limits
for k in range(num_skills):
    for i in range(num_years):
        problem += recruit_vars[k][i] <= data['recruit'][k]

# Overman constraints
for i in range(num_years):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(num_skills)) <= data['num_overman']

# Short-time working constraints
for k in range(num_skills):
    for i in range(num_years):
        problem += short_vars[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output the results
result = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(num_years)] for k in range(num_skills)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(num_years)] for k in range(num_skills)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(num_years)] for k in range(num_skills)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')