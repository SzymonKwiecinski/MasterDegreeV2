# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Translator Selection Problem}

Let:
\begin{itemize}
    \item \( N \) be the number of translators available.
    \item \( M \) be the number of required languages.
    \item \( c_i \) be the cost of hiring translator \( i \).
    \item \( S_i \) be a binary decision variable that equals 1 if translator \( i \) is selected, and 0 otherwise.
    \item \( L_i \) be the set of languages that translator \( i \) can translate.
    \item \( R \) be the set of required languages.
\end{itemize}

The objective is to minimize the total cost of hiring the translators while ensuring that all required languages can be translated.

\subsection*{Objective Function}
\[
\text{Minimize } Z = \sum_{i=1}^{N} c_i S_i
\]

\subsection*{Constraints}
\[
\sum_{i: language_m \in L_i} S_i \geq 1, \quad \forall language_m \in R
\]
This constraint ensures that at least one translator is selected for each required language.

\subsection*{Decision Variables}
\[
S_i \in \{0, 1\}, \quad \forall i = 1, 2, \ldots, N
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Translator Selection Problem}

Let:
\begin{itemize}
    \item \( N \) be the number of translators available.
    \item \( M \) be the number of required languages.
    \item \( c_i \) be the cost of hiring translator \( i \).
    \item \( S_i \) be a binary decision variable that equals 1 if translator \( i \) is selected, and 0 otherwise.
    \item \( L_i \) be the set of languages that translator \( i \) can translate.
    \item \( R \) be the set of required languages.
\end{itemize}

The objective is to minimize the total cost of hiring the translators while ensuring that all required languages can be translated.

\subsection*{Objective Function}
\[
\text{Minimize } Z = \sum_{i=1}^{N} c_i S_i
\]

\subsection*{Constraints}
\[
\sum_{i: language_m \in L_i} S_i \geq 1, \quad \forall language_m \in R
\]
This constraint ensures that at least one translator is selected for each required language.

\subsection*{Decision Variables}
\[
S_i \in \{0, 1\}, \quad \forall i = 1, 2, \ldots, N
\]

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

#### Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']

#### Number of translators
N = len(translators)

#### Create the linear programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

#### Decision variables
S = pulp.LpVariable.dicts("Translator", range(N), cat='Binary')

#### Objective function
problem += pulp.lpSum([translators[i]['cost'] * S[i] for i in range(N)]), "Total_Cost"

#### Constraints
for language in required_languages:
    problem += pulp.lpSum([S[i] for i in range(N) if language in translators[i]['languages']]) >= 1, f"Language_{language}_Requirement"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

