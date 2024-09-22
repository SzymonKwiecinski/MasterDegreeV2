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

\section*{Mathematical Model for the Translator Selection Problem}

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i$, for all $i \in T$.
    \item $A_{il}$: Indicator variable, $A_{il} = 1$ if translator $i$ can translate language $l$, $0$ otherwise, for all $i \in T$, $l \in L$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: Binary decision variable, $x_i = 1$ if translator $i$ is hired, $0$ otherwise, for all $i \in T$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{i \in T} c_i x_i
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Each required language must be covered:
    \begin{equation}
    \sum_{i \in T} A_{il} x_i \geq 1, \quad \forall l \in L
    \end{equation}
\end{itemize}

\textbf{Binary Restrictions:}
\begin{equation}
x_i \in \{0, 1\}, \quad \forall i \in T
\end{equation}

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

\section*{Mathematical Model for the Translator Selection Problem}

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i$, for all $i \in T$.
    \item $A_{il}$: Indicator variable, $A_{il} = 1$ if translator $i$ can translate language $l$, $0$ otherwise, for all $i \in T$, $l \in L$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: Binary decision variable, $x_i = 1$ if translator $i$ is hired, $0$ otherwise, for all $i \in T$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{i \in T} c_i x_i
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Each required language must be covered:
    \begin{equation}
    \sum_{i \in T} A_{il} x_i \geq 1, \quad \forall l \in L
    \end{equation}
\end{itemize}

\textbf{Binary Restrictions:}
\begin{equation}
x_i \in \{0, 1\}, \quad \forall i \in T
\end{equation}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data extracted from the provided JSON format
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

#### Sets and parameters
translators = data['translators']
required_languages = data['required_languages']

#### Create a list of translator IDs and a dictionary for their costs and language capabilities
T = [trans['id'] for trans in translators]
c = {trans['id']: trans['cost'] for trans in translators}
A = {trans['id']: [1 if lang in trans['languages'] else 0 for lang in required_languages] for trans in translators}

#### Create the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", T, cat='Binary')

#### Objective function
problem += pulp.lpSum(c[i] * x[i] for i in T)

#### Constraints to ensure all required languages are covered
for l in range(len(required_languages)):
    problem += pulp.lpSum(A[i][l] * x[i] for i in T) >= 1

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

