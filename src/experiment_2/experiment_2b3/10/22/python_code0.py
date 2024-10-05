import pulp

# Data Input
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

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function: Minimize redundancy costs
problem += pulp.lpSum(data['costredundancy'][k] * redundancy_vars[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Calculate manpower at the beginning of year i
        if i == 0:
            manpower_beginning = data['strength'][k]
        else:
            manpower_beginning = (1 - data['lessonewaste'][k]) * recruit_vars[k, i-1] + (1 - data['moreonewaste'][k]) * (
                manpower_beginning + recruit_vars[k, i-1] - redundancy_vars[k, i-1]
            )

        workforce = manpower_beginning + recruit_vars[k, i] - redundancy_vars[k, i] + overmanning_vars[k, i] + 0.5 * short_vars[k, i]

        # Requirement satisfaction
        problem += workforce >= data['requirement'][k][i]

        # Recruit limit
        problem += recruit_vars[k, i] <= data['recruit'][k]

        # Overmanning limit
        problem += pulp.lpSum(overmanning_vars[k, j] for j in range(I)) <= data['num_overman']

        # Short-time working limit
        problem += short_vars[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)],
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')