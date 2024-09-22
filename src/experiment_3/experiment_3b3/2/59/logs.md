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

\textbf{Parameters:}
\begin{itemize}
    \item Let \( N \) be the number of available translators.
    \item Let \( M \) be the number of required languages.
    \item Let \( cost_i \) represent the cost of hiring translator \( i \).
    \item Let \( languages_i \) be the set of languages that translator \( i \) can translate.
    \item Let \( required\_languages \) be the set of languages that need to be translated.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be a binary variable such that:
    \[
    x_i = 
    \begin{cases} 
    1 & \text{if translator } i \text{ is hired} \\
    0 & \text{otherwise}
    \end{cases}
    \]
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost of hiring translators:
\[
\text{Minimize } Z = \sum_{i=1}^N cost_i \cdot x_i
\]

\textbf{Constraints:}
1. Each required language must be covered by at least one selected translator:
\[
\sum_{i: language_m \in languages_i} x_i \geq 1 \quad \text{for each } m = 1, \ldots, M
\]
where \( language_m \) is each language in the \( required\_languages \).

2. \( x_i \) are binary variables:
\[
x_i \in \{0, 1\} \quad \text{for } i = 1, \ldots, N
\]

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item Selected translators: \( selected\_translators = \{ i | x_i = 1 \} \)
    \item Total cost: \( total\_cost = Z \)
\end{itemize}

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

\textbf{Parameters:}
\begin{itemize}
    \item Let \( N \) be the number of available translators.
    \item Let \( M \) be the number of required languages.
    \item Let \( cost_i \) represent the cost of hiring translator \( i \).
    \item Let \( languages_i \) be the set of languages that translator \( i \) can translate.
    \item Let \( required\_languages \) be the set of languages that need to be translated.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_i \) be a binary variable such that:
    \[
    x_i = 
    \begin{cases} 
    1 & \text{if translator } i \text{ is hired} \\
    0 & \text{otherwise}
    \end{cases}
    \]
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost of hiring translators:
\[
\text{Minimize } Z = \sum_{i=1}^N cost_i \cdot x_i
\]

\textbf{Constraints:}
1. Each required language must be covered by at least one selected translator:
\[
\sum_{i: language_m \in languages_i} x_i \geq 1 \quad \text{for each } m = 1, \ldots, M
\]
where \( language_m \) is each language in the \( required\_languages \).

2. \( x_i \) are binary variables:
\[
x_i \in \{0, 1\} \quad \text{for } i = 1, \ldots, N
\]

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item Selected translators: \( selected\_translators = \{ i | x_i = 1 \} \)
    \item Total cost: \( total\_cost = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided json
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

#### Extracting data
translators = data['translators']
required_languages = data['required_languages']
N = len(translators)  #### Number of translators

#### Creating a Linear Programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Translator", range(N), cat='Binary')

#### Objective Function
problem += pulp.lpSum([translators[i]['cost'] * x[i] for i in range(N)])

#### Constraints
for language in required_languages:
    problem += pulp.lpSum([x[i] for i in range(N) if language in translators[i]['languages']]) >= 1

#### Solve the problem
problem.solve()

#### Output results
selected_translators = [translators[i]['id'] for i in range(N) if x[i].varValue == 1]
total_cost = pulp.value(problem.objective)

print("Selected Translators:", selected_translators)
print(f"Total Cost: {total_cost}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

