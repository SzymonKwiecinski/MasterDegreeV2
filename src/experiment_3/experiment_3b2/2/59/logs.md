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

\textbf{Mathematical Model: Minimum Cost Translator Selection Problem}

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i \in T$.
    \item $a_{ij}$: Binary parameter indicating whether translator $i \in T$ can translate into language $j \in L$. 
    \begin{itemize}
        \item $a_{ij} = 1$ if translator $i$ can translate into language $j$, $0$ otherwise.
    \end{itemize}
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Binary decision variable indicating whether translator $i \in T$ is selected. 
    \begin{itemize}
        \item $x_i = 1$ if translator $i$ is selected, $0$ otherwise.
    \end{itemize}
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\min \sum_{i \in T} c_i x_i
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Ensure that for each required language at least one translator is selected:
    \begin{equation}
    \sum_{i \in T} a_{ij} x_i \geq 1, \quad \forall j \in L
    \end{equation}
    \item Binary constraints for decision variables:
    \begin{equation}
    x_i \in \{0, 1\}, \quad \forall i \in T
    \end{equation}
\end{itemize}

\end{document}
```

This mathematical model represents the problem of selecting the minimum cost team of translators to cover all required languages. The constraints ensure that each language has at least one translator, and the objective function minimizes the total cost of hiring the selected translators.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model: Minimum Cost Translator Selection Problem}

\textbf{Sets:}
\begin{itemize}
    \item $T = \{1, 2, \ldots, N\}$: Set of available translators.
    \item $L = \{1, 2, \ldots, M\}$: Set of required languages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $c_i$: Cost of hiring translator $i \in T$.
    \item $a_{ij}$: Binary parameter indicating whether translator $i \in T$ can translate into language $j \in L$. 
    \begin{itemize}
        \item $a_{ij} = 1$ if translator $i$ can translate into language $j$, $0$ otherwise.
    \end{itemize}
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Binary decision variable indicating whether translator $i \in T$ is selected. 
    \begin{itemize}
        \item $x_i = 1$ if translator $i$ is selected, $0$ otherwise.
    \end{itemize}
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\min \sum_{i \in T} c_i x_i
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Ensure that for each required language at least one translator is selected:
    \begin{equation}
    \sum_{i \in T} a_{ij} x_i \geq 1, \quad \forall j \in L
    \end{equation}
    \item Binary constraints for decision variables:
    \begin{equation}
    x_i \in \{0, 1\}, \quad \forall i \in T
    \end{equation}
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads("""
{
    "translators": [
        {"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]},
        {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]},
        {"id": 3, "cost": 13000, "languages": ["AR", "CH"]},
        {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]},
        {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]},
        {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}
    ],
    "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]
}
""")

#### Sets
translators = data['translators']
required_languages = data['required_languages']

#### Parameters
costs = {translator['id']: translator['cost'] for translator in translators}
language_capability = {translator['id']: {
    lang: 1 if lang in translator['languages'] else 0 
    for lang in required_languages
} for translator in translators}

num_translators = len(translators)
num_languages = len(required_languages)

#### Create the ILP problem
problem = pulp.LpProblem("MinCostTranslatorSelection", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", [translator['id'] for translator in translators], cat='Binary')

#### Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in costs), "Total_Cost"

#### Constraints
for j in range(num_languages):
    problem += pulp.lpSum(language_capability[i][required_languages[j]] * x[i] for i in costs) >= 1, f"Lang_{j+1}_Requirement"

#### Solve the problem
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

