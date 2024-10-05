import pulp

# Problem data
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

# Define the LP problem
problem = pulp.LpProblem("Manpower_Requirements", pulp.LpMinimize)

# Decision variables
recruit_vars = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, upBound=data['recruit'][k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning_vars = [[pulp.LpVariable(f'overmanning_{k}_{i}', lowBound=0, upBound=data['num_overman'], cat='Integer') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, upBound=data['num_shortwork'], cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimize costs
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit_vars[k][j] for j in range(i))) + 
                      data['costoverman'][k] * overmanning_vars[k][i] + 
                      data['costshort'][k] * short_vars[k][i]
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            # Initial strength for first year
            current_strength = data['strength'][k]
        else:
            # Calculated strength for subsequent years
            current_strength = (data['strength'][k] + 
                                pulp.lpSum(recruit_vars[k][j] * (1 - data['lessonewaste'][k]) for j in range(i)) + 
                                pulp.lpSum(recruit_vars[k][j] * (1 - data['moreonewaste'][k]) for j in range(i, I)))
        
        # Constraint: Workers meet or exceed requirements considering short-time and overmanning
        problem += (current_strength + overmanning_vars[k][i] + 0.5 * short_vars[k][i] >= data['requirement'][k][i])

# Solve the problem
problem.solve()

# Create output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')