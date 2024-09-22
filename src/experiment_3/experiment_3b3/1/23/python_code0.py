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

# Sets
K = range(len(data['requirement']))
I = range(len(data['requirement'][0]))

# Problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (K, I), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] * data['moreonewaste'][k] 
            + pulp.lpSum(recruit[k][i] for i in I) - pulp.lpSum(recruit[k][i] * data['moreonewaste'][k] for i in I))
            + data['costoverman'][k] * overmanning[k][i]
            + data['costshort'][k] * short[k][i] for k in K for i in I)

# Constraints
for k in K:
    problem += data['strength'][k] + pulp.lpSum(recruit[k][i] for i in I) - pulp.lpSum((1 - data['moreonewaste'][k]) * data['strength'][k] for i in I) - pulp.lpSum(short[k][i] * 0.5 for i in I) + pulp.lpSum(overmanning[k][i] for i in I) <= pulp.lpSum(data['requirement'][k][i] for i in I)

    problem += data['strength'][k] * data['lessonewaste'][k] <= pulp.lpSum(recruit[k][i] for i in I)

    problem += pulp.lpSum(recruit[k][i] for i in I) <= data['recruit'][k]

    problem += pulp.lpSum(short[k][i] for i in I) <= data['num_shortwork']

# Overmanning limit
problem += pulp.lpSum(overmanning[k][i] for k in K for i in I) <= data['num_overman']

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')