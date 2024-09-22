import pulp
import json

# Provided data in JSON format
data_json = '{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}'

# Load data from JSON
data = json.loads(data_json)

# Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']

# Sets
T = range(1, len(translators) + 1)  # Translators indexed from 1 to N
L = required_languages  # Required languages

# Parameters
costs = {translator['id']: translator['cost'] for translator in translators}
languages = {translator['id']: translator['languages'] for translator in translators}

# Create a linear programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", T, cat='Binary')

# Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in T)

# Constraints
for lang in L:
    problem += pulp.lpSum(x[i] for i in T if lang in languages[i]) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Output
selected_translators = [i for i in T if pulp.value(x[i]) == 1]
print(f'Selected Translators: {selected_translators}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')