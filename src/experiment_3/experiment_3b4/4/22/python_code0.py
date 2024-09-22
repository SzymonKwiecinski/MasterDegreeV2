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

# Constants
K = len(data['strength'])
I = len(data['requirement'][0])

# Initialize Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
R = pulp.LpVariable.dicts("Recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
O = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
S = pulp.LpVariable.dicts("Shorttime", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
Red = pulp.LpVariable.dicts("Redundancies", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * Red[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower Balance Constraint
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) - 
            data['requirement'][k][i] + 
            R[k, i] - 
            Red[k, i] + 
            O[k, i] + 
            0.5 * S[k, i] >= 0
        )
        
        # Recruitment Limit Constraint
        problem += R[k, i] <= data['recruit'][k]

        # Short-time Limit Constraint
        problem += S[k, i] <= data['num_shortwork']

# Overmanning Limit Constraint across all manpower types for each year
for i in range(I):
    problem += pulp.lpSum(O[k, i] for k in range(K)) <= data['num_overman']

# Solve Problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')