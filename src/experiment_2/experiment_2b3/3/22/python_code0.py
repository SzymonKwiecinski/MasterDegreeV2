import pulp

# Data from the input
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

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpContinuous)
overman_vars = pulp.LpVariable.dicts("Overmanning", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpContinuous)
short_vars = pulp.LpVariable.dicts("Short", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpContinuous)

# Problem
problem = pulp.LpProblem("Manpower_Minimization", pulp.LpMinimize)

# Objective: Minimize redundancy cost
redundancy_cost = [
    data['costredundancy'][k] * pulp.lpSum(recruit_vars[k, i] for i in range(I))
    for k in range(K)
]
problem += pulp.lpSum(redundancy_cost)

# Constraints
for k in range(K):
    for i in range(I):
        # Meet manpower requirements through recruitment, overmanning, and short-time work
        if i == 0:
            # Year 1: initial strength consideration
            effective_strength = data['strength'][k] * (1 - data['moreonewaste'][k])
        else:
            # Subsequent years: strength derived from previous year
            effective_strength = (data['strength'][k] 
                                  + pulp.lpSum(recruit_vars[k, j] for j in range(i)) 
                                  - pulp.lpSum(short_vars[k, j] for j in range(i)))

        problem += effective_strength + overman_vars[k, i] + 0.5 * short_vars[k, i] >= data['requirement'][k][i], f"Req_{k}_{i}"

        # Max recruitment constraints
        problem += recruit_vars[k, i] <= data['recruit'][k], f"MaxRecruit_{k}_{i}"

        # Max overmanning constraints
        problem += overman_vars[k, i] <= data['num_overman'], f"MaxOverman_{k}_{i}"

        # Max short-time work constraints
        problem += short_vars[k, i] <= data['num_shortwork'], f"MaxShort_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overman_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')