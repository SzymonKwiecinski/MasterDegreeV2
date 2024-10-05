import pulp

# Parsing the provided data
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

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Initialize the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize costs
objective = []
for k in range(K):
    for i in range(I):
        objective.append(data['costredundancy'][k] * recruit_vars[k, i])
        objective.append(data['costoverman'][k] * overmanning_vars[k, i])
        objective.append(data['costshort'][k] * short_vars[k, i])

problem += pulp.lpSum(objective)

# Constraints
for k in range(K):
    for i in range(I):
        # Inventory balance equation considering wastage
        if i == 0:
            initial_strength = data['strength'][k]
            current_inventory = recruit_vars[k, i] + initial_strength * (1 - data['moreonewaste'][k])
        else:
            current_inventory = (
                recruit_vars[k, i]
                + (recruit_vars[k, i-1] * (1 - data['lessonewaste'][k]))  # Wastage for less than one year's service
                + (data['strength'][k] * (1 - data['moreonewaste'][k]))  # Wastage for more than one year's service
            )
        
        # Meeting the manpower requirements with optional overmanning and short-time working
        problem += current_inventory + overmanning_vars[k, i] + (short_vars[k, i] / 2) == data['requirement'][k][i]

        # Recruitment limits
        problem += recruit_vars[k, i] <= data['recruit'][k]

        # Overmanning limits
        problem += pulp.lpSum(overmanning_vars[k, j] for j in range(I)) <= data['num_overman']

        # Short-time limits
        problem += short_vars[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output results
result = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]
}

print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')