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

I = len(data['requirement'][0])
K = len(data['strength'])

# Initialize LP model
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
r = pulp.LpVariable.dicts("r", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * r[(k, i)] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    # Overmanning Limit
    problem += pulp.lpSum(y[(k, i)] for k in range(K)) <= data['num_overman']
    
    for k in range(K):
        # Balance of Manpower
        if i == 0:
            previous_x, previous_r = 0, 0
        else:
            previous_x, previous_r = x[(k, i-1)], r[(k, i-1)]
        
        lhs = (data['strength'][k] + x[(k, i)] - r[(k, i)]
               - data['lessonewaste'][k] * x[(k, i)]
               - data['moreonewaste'][k] * (data['strength'][k] + previous_x - previous_r)
               + y[(k, i)] + 0.5 * z[(k, i)])
        
        rhs = data['requirement'][k][i]
        problem += (lhs == rhs)
        
        # Recruitment Limit
        problem += x[(k, i)] <= data['recruit'][k]
        
        # Short-time working Limit
        problem += z[(k, i)] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')