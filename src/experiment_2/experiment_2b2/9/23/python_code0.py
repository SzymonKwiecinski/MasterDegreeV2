import pulp

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

num_skills = len(data['strength'])
num_years = len(data['requirement'][0])

# Problem definition
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(num_skills) for i in range(num_years)), 0)
overman_vars = pulp.LpVariable.dicts("Overman", ((k, i) for k in range(num_skills) for i in range(num_years)), 0, data['num_overman'])
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(num_skills) for i in range(num_years)), 0, data['num_shortwork'])

# Objective function: Minimize total cost
problem += (
    pulp.lpSum(
        recruit_vars[k, i] * 0  # Recruitment assumed to have no cost impact directly in provided info
        + overman_vars[k, i] * data['costoverman'][k]
        + short_vars[k, i] * data['costshort'][k] 
        for k in range(num_skills)
        for i in range(num_years)
    )
)

# Constraints
for k in range(num_skills):
    for i in range(num_years):
        if i == 0:
            # First year starts with initial manpower
            manpower = data['strength'][k]
        else:
            # Subsequent years consider recruits and wastage
            manpower = (
                manpower
                + recruit_vars[k, i-1] * (1 - data['lessonewaste'][k])
                - recruit_vars[k, i-1] * data['lessonewaste'][k]
                - data['strength'][k] * data['moreonewaste'][k]
            )
        
        problem += (
            manpower + overman_vars[k, i] + short_vars[k, i] * 0.5 
            >= data['requirement'][k][i]
        )
        
        problem += recruit_vars[k, i] <= data['recruit'][k]

# Solve the problem
problem.solve()

# Output results
output = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(num_years)] for k in range(num_skills)],
    "overmanning": [[pulp.value(overman_vars[k, i]) for i in range(num_years)] for k in range(num_skills)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(num_years)] for k in range(num_skills)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')