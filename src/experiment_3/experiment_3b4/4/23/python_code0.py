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

num_categories = len(data['strength'])
num_years = len(data['requirement'][0])

# Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(num_categories) for i in range(num_years)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k, i] +
                      data['costoverman'][k] * overmanning[k, i] +
                      data['costshort'][k] * short[k, i]
                      for k in range(num_categories) for i in range(num_years))

# Constraints

# Manpower Balance Constraints
for k in range(num_categories):
    # Current balance
    problem += data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit[k, 0] - redundancy[k, 0] + overmanning[k, 0] == data['strength'][k]
    
    # Future balance
    balance = {0: data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit[k, 0] - redundancy[k, 0] + overmanning[k, 0]}
    for i in range(1, num_years):
        balance[i] = (1 - data['lessonewaste'][k]) * recruit[k, i-1] + (1 - data['moreonewaste'][k]) * balance[i-1] + recruit[k, i] - redundancy[k, i] + overmanning[k, i]
        problem += balance[i] == balance[i]

    # Meeting Requirements
    for i in range(num_years):
        problem += balance[i] + 0.5 * short[k, i] >= data['requirement'][k][i]

# Limits and Bounds
for k in range(num_categories):
    for i in range(num_years):
        problem += recruit[k, i] <= data['recruit'][k]
        problem += short[k, i] <= data['num_shortwork']
        
    problem += pulp.lpSum(overmanning[k, i] for i in range(num_years)) <= data['num_overman']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')