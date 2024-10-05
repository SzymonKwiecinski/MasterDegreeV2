import pulp

# Load data
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

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + recruit[(k, i)] - data['requirement'][k][i] 
                                                    - overmanning[(k, i)] - 0.5 * short[(k, i)]) 
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance constraint
        problem += (data['strength'][k] + recruit[(k, i)] - (data['strength'][k] * (1 - data['lessonewaste'][k]) * (1 - data['moreonewaste'][k])) 
                     - short[(k, i)] <= data['requirement'][k][i] + overmanning[(k, i)])
        
        # Recruitment limit
        problem += recruit[(k, i)] <= data['recruit'][k]
        
        # Short-time working limit
        problem += short[(k, i)] <= data['num_shortwork']

for i in range(I):
    # Overmanning limit
    problem += pulp.lpSum(overmanning[(k, i)] for k in range(K)) <= data['num_overman']

# Solve the problem
problem.solve()

# Print the outputs
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')