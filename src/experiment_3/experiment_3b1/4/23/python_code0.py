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

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i]) 
                       for k in range(K) for i in range(I) if data['strength'][k] - data['requirement'][k][i] > 0) + \
              pulp.lpSum(data['costoverman'][k] * overmanning_vars[k, i] 
                          for k in range(K) for i in range(I)) + \
              pulp.lpSum(data['costshort'][k] * short_vars[k, i] 
                          for k in range(K) for i in range(I))

# Constraints

# Manpower balance
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + 
                     pulp.lpSum(recruit_vars[k, j] for j in range(I)) - 
                     (data['lessonewaste'][k] * recruit_vars[k, i] + 
                      data['moreonewaste'][k] * (data['strength'][k] - overmanning_vars[k, i] - short_vars[k, i]))) >= \
                     data['requirement'][k][i] - overmanning_vars[k, i] - 0.5 * short_vars[k, i]

# Recruitment limit
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k, i] <= data['recruit'][k]

# Overmanning limit
problem += pulp.lpSum(overmanning_vars[k, i] for k in range(K) for i in range(I)) <= data['num_overman']

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += short_vars[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output the results
recruit_result = [[recruit_vars[k, i].varValue for i in range(I)] for k in range(K)]
overmanning_result = [[overmanning_vars[k, i].varValue for i in range(I)] for k in range(K)]
short_result = [[short_vars[k, i].varValue for i in range(I)] for k in range(K)]

print(f'Recruit Results: {recruit_result}')
print(f'Overmanning Results: {overmanning_result}')
print(f'Short-time Working Results: {short_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')