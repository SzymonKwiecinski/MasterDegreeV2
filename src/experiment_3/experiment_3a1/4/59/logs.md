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
    \item Let \( N \) be the total number of available translators.
    \item Let \( M \) be the total number of required languages.
    \item Let \( \text{cost}_i \) be the cost of hiring translator \( i \).
    \item Let \( \text{languages}_i \) be the set of languages that translator \( i \) can translate into.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \in \{0, 1\} \) be a binary variable where 
        \[
        x_i = \begin{cases} 
        1 & \text{if translator } i \text{ is selected} \\ 
        0 & \text{otherwise}
        \end{cases}
        \]
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{i=1}^{N} \text{cost}_i \cdot x_i
\]

\textbf{Constraints:}
\begin{itemize}
    \item Each required language must be covered by at least one selected translator:
    \[
    \sum_{i: \text{language}_m \in \text{languages}_i} x_i \geq 1, \quad \forall m = 1, \ldots, M
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \( \text{selected\_translators} = \{i : x_i = 1\} \)
    \item \( \text{total\_cost} = Z \)
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
    \item Let \( N \) be the total number of available translators.
    \item Let \( M \) be the total number of required languages.
    \item Let \( \text{cost}_i \) be the cost of hiring translator \( i \).
    \item Let \( \text{languages}_i \) be the set of languages that translator \( i \) can translate into.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_i \in \{0, 1\} \) be a binary variable where 
        \[
        x_i = \begin{cases} 
        1 & \text{if translator } i \text{ is selected} \\ 
        0 & \text{otherwise}
        \end{cases}
        \]
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{i=1}^{N} \text{cost}_i \cdot x_i
\]

\textbf{Constraints:}
\begin{itemize}
    \item Each required language must be covered by at least one selected translator:
    \[
    \sum_{i: \text{language}_m \in \text{languages}_i} x_i \geq 1, \quad \forall m = 1, \ldots, M
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \( \text{selected\_translators} = \{i : x_i = 1\} \)
    \item \( \text{total\_cost} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

#### Problem definition
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(len(data['translators'])), cat='Binary')

#### Objective Function
problem += pulp.lpSum(translator['cost'] * x[i] for i, translator in enumerate(data['translators'])), "Total_Cost"

#### Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(x[i] for i, translator in enumerate(data['translators']) if language in translator['languages']) >= 1, f"Cover_{language}"

#### Solve the problem
problem.solve()

#### Output
selected_translators = [i + 1 for i in range(len(data['translators'])) if pulp.value(x[i]) == 1]
total_cost = pulp.value(problem.objective)
print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

