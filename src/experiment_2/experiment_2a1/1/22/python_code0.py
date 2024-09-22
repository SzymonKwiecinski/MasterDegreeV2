import pulp
import json

data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
        'strength': [2000, 1500, 1000], 
        'lessonewaste': [0.25, 0.2, 0.1], 
        'moreonewaste': [0.1, 0.05, 0.05], 
        'recruit': [500, 800, 500], 
        'costredundancy': [200, 500, 500], 
        'num_overman': 150, 
        'costoverman': [1500, 2000, 3000], 
        'num_shortwork': 50, 
        'costshort': [500, 400, 400]}

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=1500, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, upBound=data['num_overman'], cat='Integer')
short = pulp.LpVariable.dicts("ShortTime", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit[k][i] for i in range(I)) - pulp.lpSum(data['requirement'][k][i] + overmanning[k][i] - short[k][i] / 2 for i in range(I))) for k in range(K))

# Constraints
for k in range(K):
    for i in range(I):
        # Strength after recruitment and wastage
        problem += (data['strength'][k] + pulp.lpSum(recruit[k][j] for j in range(i+1)) - pulp.lpSum(overmanning[k][i] for j in range(I)) - short[k][i] / 2 >= data['requirement'][k][i], f"Manpower_Requirement_{k}_{i}")
        # Limit on recruitment
        problem += (pulp.lpSum(recruit[k][j] for j in range(I)) <= data['recruit'][k], f"Recruitment_Limit_{k}")

# Solve the problem
problem.solve()

# Output the results
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')