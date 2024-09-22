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

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * (- data['lessonewaste'][k] * data['strength'][k] - data['moreonewaste'][k] * data['strength'][k] + recruit_vars[(k, i)])
    + data['costoverman'][k] * overmanning_vars[(k, i)] 
    + data['costshort'][k] * short_vars[(k, i)]
    for k in range(K) for i in range(I)
)

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance
        problem += (
            data['strength'][k] - data['lessonewaste'][k] * data['strength'][k] - data['moreonewaste'][k] * data['strength'][k] 
            + recruit_vars[(k, i)] + overmanning_vars[(k, i)] - short_vars[(k, i)] 
            >= data['requirement'][k][i]
        )
        # Recruitment limits
        problem += (
            recruit_vars[(k, i)] <= data['recruit'][k]
        )
        # Short-time working limits
        problem += (
            short_vars[(k, i)] <= data['num_shortwork']
        )

for i in range(I):
    # Overmanning limits
    problem += (
        pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman']
    )

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')