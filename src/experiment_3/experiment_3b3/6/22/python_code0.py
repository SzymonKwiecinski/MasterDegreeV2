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

# Sets
K = range(len(data['strength']))  # Manpower categories
I = range(len(data['requirement'][0]))  # Years

# Problem definition
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (K, I), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (recruit[k][i] - data['requirement'][k][i] + short[k][i] - overmanning[k][i])
                      + data['costoverman'][k] * overmanning[k][i]
                      + data['costshort'][k] * short[k][i]
                      for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit[k][i] + overmanning[k][i] - short[k][i]
            >= data['requirement'][k][i], f"ManpowerRequirement_{k}_{i}"
        )
        problem += recruit[k][i] <= data['recruit'][k], f"RecruitmentLimit_{k}_{i}"
        problem += short[k][i] <= data['num_shortwork'], f"ShortTimeWorkingLimit_{k}_{i}"

for i in I:
    problem += (
        pulp.lpSum(overmanning[k][i] for k in K) <= data['num_overman'], f"OvermanningLimit_{i}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')