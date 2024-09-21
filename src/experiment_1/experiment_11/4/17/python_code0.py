import pulp
import json

# Data provided in JSON format
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Number of translators and required languages
N = len(data['translators'])
M = len(data['required_languages'])

# Create the linear programming problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')

# Objective function: Minimize the total cost of hiring translators
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i] for i in range(N)), "Total_Cost"

# Constraints: Each required language must be covered by at least one hired translator
for j in range(M):
    lang = data['required_languages'][j]
    problem += pulp.lpSum(x[i] for i in range(N) if lang in data['translators'][i]['languages']) >= 1, f"Language_Coverage_{lang}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')