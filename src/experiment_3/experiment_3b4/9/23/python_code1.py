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

categories = range(len(data['strength']))  # K
years = range(len(data['requirement'][0]))  # I

# Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (categories, years), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (categories, years), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (categories, years), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", (categories, years), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['costoverman'][k] * overmanning[k][i] +
    data['costredundancy'][k] * redundancy[k][i] +
    data['costshort'][k] * short[k][i]
    for k in categories for i in years
)

# Constraints
for k in categories:
    for i in years:
        # Available Manpower Constraint
        available_manpower = sum((1 - data['moreonewaste'][k])**j * data['strength'][k] for j in range(i+1)) \
                            + recruit[k][i] - redundancy[k][i] - (short[k][i] / 2) + overmanning[k][i]
        problem += available_manpower >= data['requirement'][k][i], f"ManpowerBalance_{k}_{i}"

        # Recruitment Limit
        problem += recruit[k][i] <= data['recruit'][k], f"RecruitmentLimit_{k}_{i}"

        # Short-time Working Limit
        problem += short[k][i] <= data['num_shortwork'], f"ShortTimeWorkingLimit_{k}_{i}"

for i in years:
    # Overmanning Limit
    problem += pulp.lpSum(overmanning[k][i] for k in categories) <= data['num_overman'], f"OvermanningLimit_{i}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')