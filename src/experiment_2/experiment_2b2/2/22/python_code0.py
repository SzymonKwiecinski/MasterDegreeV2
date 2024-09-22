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

K = len(data['strength'])
I = len(data['requirement'][0])

# LP Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Initial Workers
workers = [[pulp.LpVariable(f'Workers_{k}_{i}', lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]

# Objective
problem += pulp.lpSum(redundancy[k, i] * data['costredundancy'][k] for k in range(K) for i in range(I)), "Total Cost of Redundancy"

# Constraints
for k in range(K):
    for i in range(I):
        # Workforce balance constraints
        if i == 0:
            problem += (
                workers[k][i] == (data['strength'][k] + recruit[k, i] - redundancy[k, i] - overmanning[k, i] - short[k, i]/2) * (1 - data['moreonewaste'][k])
            ), f"Workforce_Balance_{k}_{i}"
        else:
            problem += (
                workers[k][i] == (workers[k][i-1] + recruit[k, i] - redundancy[k, i] - overmanning[k, i] - short[k, i]/2) * (1 - data['moreonewaste'][k])
            ), f"Workforce_Balance_{k}_{i}"

        # Requirement Satisfaction
        problem += workers[k][i] + overmanning[k, i] + short[k, i]/2 >= data['requirement'][k][i], f"Requirement_{k}_{i}"

    # Recruitment Constraints
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k], f"Recruitment_Limit_{k}_{i}"
    
    # Overmanning Constraints
    for i in range(I):
        problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'], f"Overmanning_Limit_{i}"
    
    # Short-Time Working Constraints
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork'], f"ShortTime_Limit_{k}_{i}"

# Solve
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')