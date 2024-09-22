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

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i$.
    \item $S_i \subseteq L$: Set of languages that translator $i$ can translate.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i \in \{0, 1\}$: Indicator variable for translator $i$, where $1$ means translator $i$ is selected, and $0$ otherwise.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{i \in T} c_i x_i
\]

\textbf{Constraints:}
\begin{itemize}
    \item Ensure that all required languages are covered:
    \[
    \sum_{i \in T: j \in S_i} x_i \geq 1, \quad \forall j \in L
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item Selected translators: $x_i$ where $x_i = 1$.
    \item Total cost: $Z$.
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

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i$.
    \item $S_i \subseteq L$: Set of languages that translator $i$ can translate.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i \in \{0, 1\}$: Indicator variable for translator $i$, where $1$ means translator $i$ is selected, and $0$ otherwise.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{i \in T} c_i x_i
\]

\textbf{Constraints:}
\begin{itemize}
    \item Ensure that all required languages are covered:
    \[
    \sum_{i \in T: j \in S_i} x_i \geq 1, \quad \forall j \in L
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item Selected translators: $x_i$ where $x_i = 1$.
    \item Total cost: $Z$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Provided data in JSON format
data_json = '{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}'

#### Load data from JSON
data = json.loads(data_json)

#### Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']

#### Sets
T = range(1, len(translators) + 1)  #### Translators indexed from 1 to N
L = required_languages  #### Required languages

#### Parameters
costs = {translator['id']: translator['cost'] for translator in translators}
languages = {translator['id']: translator['languages'] for translator in translators}

#### Create a linear programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", T, cat='Binary')

#### Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in T)

#### Constraints
for lang in L:
    problem += pulp.lpSum(x[i] for i in T if lang in languages[i]) >= 1, f"Cover_{lang}"

#### Solve the problem
problem.solve()

#### Output
selected_translators = [i for i in T if pulp.value(x[i]) == 1]
print(f'Selected Translators: {selected_translators}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

