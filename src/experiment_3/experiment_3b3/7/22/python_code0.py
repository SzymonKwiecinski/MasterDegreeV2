import pulp

# Data from the JSON
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'num_shortwork': 50
}

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
r = pulp.LpVariable.dicts("Recruit", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Integer')
o = pulp.LpVariable.dicts("Overman", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("ShortTime", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Integer')
d = pulp.LpVariable.dicts("Redundancy", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * d[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += r[k, i] <= data['recruit'][k]

        problem += s[k, i] <= data['num_shortwork']

    for i in range(I):
        if i == 0:
            s_prev = 0
        else:
            s_prev = (1 - data['lessonewaste'][k]) * s[k, i - 1]

        manpower_expression = (data['strength'][k] - s_prev 
                               - data['moreonewaste'][k] * data['strength'][k]
                               + r[k, i] - d[k, i] + o[k, i])

        problem += manpower_expression >= data['requirement'][k][i]

for i in range(I):
    problem += pulp.lpSum(o[k, i] for k in range(K)) <= data['num_overman']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')