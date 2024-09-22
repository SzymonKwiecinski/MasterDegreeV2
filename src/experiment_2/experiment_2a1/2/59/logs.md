# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO:

- A team of translators is being assem- bled for the summer Olympics to translate from English into the \{M} other languages.
- There is a pool of \var{N} translators available.
- Each translator \var{i} can translate into a certain set of \var{languages} and comes with a specific \var{cost_i}.

INPUT FORMAT: 

{
"translators": [
        {"id": i, 
         "cost": cost_i,
         "languages": [language_j for j in 1, ..., L_i]
        },
        for n in 1, ..., N
    ],
    "required_languages": [language_m for m in 1, ..., M]
}

OBJECTIVE: Select the combination of translators that ensures all required languages can be translated into, at the minimum possible cost.

OUTPUT INFO:

- \var{selected_translators} represents the list of translators chosen.
- \var{total_cost} shows the total cost for hiring the selected translators.

OUTPUT FORMAT:

{
    "selected_translators": [translator_ids],
    "total_cost": total_cost
}
</DESCRIPTION>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}],
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

#### Problem definition
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

#### Variables
translator_vars = pulp.LpVariable.dicts("Translators", [t['id'] for t in data['translators']], 
                                          cat='Binary')

#### Objective function
problem += pulp.lpSum([t['cost'] * translator_vars[t['id']] for t in data['translators']])

#### Constraints
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[t['id']] for t in data['translators'] 
                           if language in t['languages']]) >= 1, f"Lang_{language}"

#### Solve the problem
problem.solve()

#### Selected translators and total cost
selected_translators = [t['id'] for t in data['translators'] if translator_vars[t['id']].value() == 1]
total_cost = pulp.value(problem.objective)

#### Output format
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

