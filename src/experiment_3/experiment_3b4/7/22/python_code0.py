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

# Parameters
K = 3  # Number of manpower categories
I = 3  # Number of years

# Problem
problem = pulp.LpProblem("Manpower_Requirements", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(redundancy[k, i] * data['costredundancy'][k] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower Balance Constraints
        if i == 0:
            prev_recruit_sum = 0
        else:
            prev_recruit_sum = pulp.lpSum(recruit[k, j] * (1 - data['lessonewaste'][k]) for j in range(i))
            
        problem += (data['strength'][k] + prev_recruit_sum - redundancy[k, i] - 
                    data['moreonewaste'][k] * (data['strength'][k] + pulp.lpSum(recruit[k, j] for j in range(i))) +
                    overmanning[k, i] + 0.5 * short[k, i] == data['requirement'][k][i])

        # Recruitment Constraints
        problem += recruit[k, i] <= data['recruit'][k]

        # Redundancy Constraints
        problem += redundancy[k, i] >= 0

    # Overmanning Constraints
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman']

    # Short-Time Working Constraints
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')