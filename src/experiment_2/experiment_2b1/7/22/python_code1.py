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

# Model
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')
short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + 
                 pulp.lpSum(recruit[k][i] for i in range(I)) + 
                 pulp.lpSum(overmanning[k][i] for i in range(I)) - 
                 pulp.lpSum(short[k][i] for i in range(I)) - 
                 data['requirement'][k][i] for k in range(K) for i in range(I)))

# Constraints
for k in range(K):
    for i in range(I):
        # Maximum recruits
        problem += recruit[k][i] <= data['recruit'][k], f"MaxRecruit_k{k}_i{i}"
        
        # Overmanning limit
        problem += pulp.lpSum(overmanning[k][j] for j in range(I)) <= data['num_overman'], f"MaxOverman_k{k}"
        
        # Short-time working limit
        problem += short[k][i] <= data['num_shortwork'], f"MaxShort_k{k}_i{i}"

# Wastage calculations
for k in range(K):
    for i in range(I):
        if i == 0:  # First year
            problem += (data['strength'][k] - short[k][i] - pulp.lpSum(recruit[k][j] for j in range(i + 1)) + 
                         (data['strength'][k] * (1 - data['lessonewaste'][k])) >= data['requirement'][k][i], 
                         f"WastageYear1_k{k}_i{i}")
        else:  # Subsequent years
            problem += (data['strength'][k] - short[k][i] - pulp.lpSum(recruit[k][j] for j in range(i + 1)) + 
                         (data['strength'][k] * (1 - data['moreonewaste'][k])) >= data['requirement'][k][i], 
                         f"WastageYear_k{k}_i{i}")

# Solve the problem
problem.solve()

# Collecting results
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')