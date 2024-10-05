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

# Indices
K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
x_recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Integer')
x_overman = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
x_short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Integer')
x_redundancy = pulp.LpVariable.dicts("Redundancy", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function: Minimize redundancy cost
problem += pulp.lpSum(x_redundancy[k][i] * data['costredundancy'][k] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        if i == 0:
            # First year manpower balance
            manpower_balance = data['strength'][k] * (1 - data['moreonewaste'][k])
        else:
            # Subsequent years manpower balance
            manpower_balance = (1 - data['lessonewaste'][k]) * x_recruit[k][i-1] + (1 - data['moreonewaste'][k]) * (current_strength[k] - x_redundancy[k][i-1])

        manpower_balance += x_recruit[k][i] + x_overman[k][i] + 0.5 * x_short[k][i]
        
        problem += manpower_balance >= data['requirement'][k][i]

        # Constraints for overmanning and short-time working
        problem += x_overman[k][i] <= data['num_overman']
        problem += x_short[k][i] <= data['num_shortwork']
        problem += x_recruit[k][i] <= data['recruit'][k]
        
        # Redundancy calculation
        current_strength = [data['strength'][k] for k in range(K)]
        problem += x_redundancy[k][i] == current_strength[k] + x_recruit[k][i] + x_overman[k][i] - data['requirement'][k][i]

# Solve Problem
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(x_recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(x_overman[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(x_short[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')