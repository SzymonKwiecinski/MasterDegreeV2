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

# Problem Initialization
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Parameters
K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=[data['recruit'][k] for k in range(K)], cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective Function
costs = pulp.lpSum(
    recruit[k][i] * 0 +  # No cost for recruit since they are considered for recruitment limits
    overmanning[k][i] * data['costoverman'][k] +
    short[k][i] * data['costshort'][k]
    for k in range(K) for i in range(I)
)

problem += costs

# Constraints
for i in range(I):
    for k in range(K):
        problem += pulp.lpSum(recruit[k][j] for j in range(i + 1)) + data['strength'][k] * (1 - data['moreonewaste'][k]) - overmanning[k][i] - short[k][i] >= data['requirement'][k][i], f"Manpower_Requirement_{k}_{i}"

    # Overmanning constraint
    problem += pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman'], f"Total_Overmanning_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')