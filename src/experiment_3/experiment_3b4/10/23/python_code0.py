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

# Indices for manpower categories and years
K = len(data['strength'])  # number of manpower categories
I = len(data['requirement'][0])  # number of years

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Labour_Costs", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundant = pulp.LpVariable.dicts("redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
employed = pulp.LpVariable.dicts("employed", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * redundant[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
), "Total Cost"

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower Balancing
        if i == 0:
            problem += employed[k, i] == data['strength'][k], f"Initial_Employed_{k}_{i}"
        else:
            problem += employed[k, i] == (
                (1 - data['moreonewaste'][k]) * (employed[k, i - 1] - redundant[k, i - 1]) +
                (1 - data['lessonewaste'][k]) * recruit[k, i - 1]
            ), f"Employed_Balance_{k}_{i}"

        # Requirement Fulfillment
        problem += employed[k, i] + overmanning[k, i] + 0.5 * short[k, i] >= data['requirement'][k][i], f"Requirement_{k}_{i}"

        # Recruitment Limitation
        problem += recruit[k, i] <= data['recruit'][k], f"Recruit_Limit_{k}_{i}"

        # Short-time Working Limitation
        problem += short[k, i] <= data['num_shortwork'], f"Short_Limit_{k}_{i}"

# Overmanning Limitation
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'], f"Overman_Limit_{i}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
