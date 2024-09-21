# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Hiring Translators}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of translators
    \item $M$: Number of required languages
    \item $Cost_i$: Cost of hiring translator $i$, for $i = 1, 2, \ldots, N$
    \item $Languages_i$: Set of languages that translator $i$ can translate, for $i = 1, 2, \ldots, N$
    \item $RequiredLanguages$: List of required languages, indexed by $j = 1, 2, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Binary variable indicating whether translator $i$ is hired (1) or not (0), for $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of hiring translators:
\[
\min \sum_{i=1}^{N} Cost_i \cdot x_i
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each required language must be covered by at least one hired translator:
    \[
    \forall j \in \{1, 2, \ldots, M\}, \quad \sum_{i: j \in Languages_i} x_i \geq 1
    \]
    \item Binary constraints for decision variables:
    \[
    \forall i \in \{1, 2, \ldots, N\}, \quad x_i \in \{0, 1\}
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000,  'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000,  'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

translators = data['translators']
required_languages = data['required_languages']

#### Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

#### Decision Variables
translator_vars = pulp.LpVariable.dicts("hire", [t['id'] for t in translators], cat='Binary')

#### Objective Function
problem += pulp.lpSum(t['cost'] * translator_vars[t['id']] for t in translators)

#### Constraints
for lang in required_languages:
    problem += (
        pulp.lpSum(translator_vars[t['id']] for t in translators if lang in t['languages']) >= 1,
        f"Lang_{lang}_Coverage"
    )

#### Solve
problem.solve()

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

