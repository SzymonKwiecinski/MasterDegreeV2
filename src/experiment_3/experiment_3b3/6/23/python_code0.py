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

K = len(data['strength'])  # Total number of manpower categories
I = len(data['requirement'][0])  # Total number of years

# Initialize the problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * redundancy_vars[k, i] +
    data['costoverman'][k] * overmanning_vars[k, i] +
    data['costshort'][k] * short_vars[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] -
            (data['lessonewaste'][k] * recruit_vars[k, i] +
             data['moreonewaste'][k] * data['strength'][k] -
             redundancy_vars[k, i] +
             short_vars[k, i] / 2 +
             overmanning_vars[k, i])
            == data['requirement'][k][i]
        ), f"Manpower_Requirement_{k}_{i}"

        problem += recruit_vars[k, i] <= data['recruit'][k], f"Recruit_Limit_{k}_{i}"
        problem += short_vars[k, i] <= data['num_shortwork'], f"Shortwork_Limit_{k}_{i}"

for i in range(I):
    problem += (
        pulp.lpSum(overmanning_vars[k, i] for k in range(K)) <= data['num_overman']
    ), f"Overmanning_Limit_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')