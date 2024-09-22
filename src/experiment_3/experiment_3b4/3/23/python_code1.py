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

# Parameters
K = len(data['strength'])
I = len(data['requirement'][0])

# Decision Variables
r = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(1, I+1)), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("overman", ((k, i) for k in range(K) for i in range(1, I+1)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(1, I+1)), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("staff", ((k, i) for k in range(K) for i in range(I+1)), lowBound=0, cat='Continuous')

# Linear Programming Problem
problem = pulp.LpProblem("Minimize_Manpower_Costs", pulp.LpMinimize)

# Initial Conditions
for k in range(K):
    problem += x[k, 0] == data['strength'][k]

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * r[k, i] + data['costoverman'][k] * o[k, i] + data['costshort'][k] * s[k, i]
    for k in range(K) for i in range(1, I+1)
)

# Constraints
for k in range(K):
    for i in range(1, I+1):
        if i == 1:
            problem += x[k, i] == x[k, 0] * (1 - data['moreonewaste'][k]) + r[k, i] * (1 - data['lessonewaste'][k])
        else:
            problem += x[k, i] == x[k, i-1] * (1 - data['moreonewaste'][k]) + r[k, i] * (1 - data['lessonewaste'][k])

        problem += (x[k, i] + o[k, i] + (s[k, i] / 2)) >= data['requirement'][k][i-1]
        problem += o[k, i] <= data['num_overman']
        problem += s[k, i] <= data['num_shortwork']
        problem += r[k, i] <= data['recruit'][k]

# Solving the problem
problem.solve()

# Printing the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')