import pulp
import json

# Load data
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

# Extracting data
translators = data['translators']
required_languages = data['required_languages']

# Parameters
N = len(translators)
M = len(required_languages)
Cost = {translator['id']: translator['cost'] for translator in translators}
Languages = {translator['id']: set(translator['languages']) for translator in translators}

# Problem Definition
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [translator['id'] for translator in translators], cat='Binary')

# Objective Function
problem += pulp.lpSum(Cost[i] * x[i] for i in Cost), "Total_Cost"

# Constraints
for lang in required_languages:
    problem += pulp.lpSum(x[i] for i in Cost if lang in Languages[i]) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')