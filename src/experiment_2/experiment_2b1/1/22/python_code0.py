import pulp
import json

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

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=[data['recruit'][k] for k in range(K)], cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - pulp.lpSum(recruit[k][i] for i in range(I)) - overmanning[k][i] - short[k][i]/2) for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance
        problem += (data['strength'][k] - pulp.lpSum(recruit[k][j] for j in range(i+1)) - 
                     pulp.lpSum(short[k][j] for j in range(i+1))/2 - 
                     pulp.lpSum(overmanning[k][j] for j in range(i+1)) -
                     (data['lessonewaste'][k] * recruit[k][0] if i == 0 else data['moreonewaste'][k] * (data['strength'][k] - pulp.lpSum(recruit[k][j] for j in range(i))) )
                     ) >= data['requirement'][k][i]
                     )

        # Overmanning limit
        problem += pulp.lpSum(overmanning[k][j] for j in range(I)) <= data['num_overman']

# Solve the problem
problem.solve()

# Output the results
recruit_result = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_result = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_result = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(json.dumps(output, indent=4))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')