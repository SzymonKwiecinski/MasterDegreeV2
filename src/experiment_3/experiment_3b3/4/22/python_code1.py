import pulp

# Data from JSON format
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

# Parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Define the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] - overmanning[k, i] - short[k, i] / 2)
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance constraint
        problem += (data['strength'][k] - (1 - data['lessonewaste'][k]) * recruit[k, i] - (1 - data['moreonewaste'][k]) * data['strength'][k]
                    >= data['requirement'][k][i] + overmanning[k, i] + short[k, i] / 2)

        # Recruitment limits
        problem += recruit[k, i] <= data['recruit'][k]

        # Short-time working limits
        problem += short[k, i] <= data['num_shortwork']

# Overmanning limits
problem += pulp.lpSum(overmanning[k, i] for k in range(K) for i in range(I)) <= data['num_overman']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')