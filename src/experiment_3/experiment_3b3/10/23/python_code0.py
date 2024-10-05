import pulp

# Data from JSON
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

# Indices
categories = range(len(data['strength']))
years = range(len(data['requirement'][0]))

# Problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", (categories, years), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", (categories, years), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", (categories, years), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * pulp.lpSum([max(0, data['strength'][k] - data['requirement'][k][i]) for i in years]) +
    data['costoverman'][k] * overmanning[k][i] +
    data['costshort'][k] * short[k][i]
    for k in categories for i in years
)

# Constraints

# Manpower Balance
for k in categories:
    for i in years:
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) +
            recruit[k][i] * (1 - data['lessonewaste'][k]) + overmanning[k][i] - short[k][i]
            >= data['requirement'][k][i]
        )

# Recruitment Limits
for k in categories:
    for i in years:
        problem += recruit[k][i] <= data['recruit'][k]

# Overmanning Limits
for i in years:
    problem += pulp.lpSum(overmanning[k][i] for k in categories) <= data['num_overman']

# Short-time Working Limits
for k in categories:
    for i in years:
        problem += short[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')