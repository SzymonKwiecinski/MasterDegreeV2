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

\section*{Mathematical Model for Translator Selection}

\subsection*{Sets}
\begin{itemize}
    \item Let \( T = \{1, 2, \ldots, N\} \) be the set of available translators.
    \item Let \( L = \{1, 2, \ldots, M\} \) be the set of required languages.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cost}_i \): Cost of hiring translator \( i \in T \).
    \item \( S_i \): Set of languages that translator \( i \) can translate (subset of \( L \)).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \) be a binary variable such that:
    \[
    x_i = 
    \begin{cases} 
    1 & \text{if translator } i \text{ is selected} \\ 
    0 & \text{otherwise} 
    \end{cases}
    \]
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of selected translators:
\[
\text{Minimize } Z = \sum_{i \in T} \text{cost}_i \cdot x_i
\]

\subsection*{Constraints}
Ensure all required languages are covered:
\[
\sum_{i \in T} x_i \cdot \mathbb{I}(j \in S_i) \geq 1 \quad \forall j \in L
\]
where \( \mathbb{I}(j \in S_i) \) is an indicator function that is 1 if language \( j \) is in the set of languages that translator \( i \) can translate, and 0 otherwise.

\subsection*{Binary Constraints}
\[
x_i \in \{0, 1\} \quad \forall i \in T
\]

\subsection*{Output}
\begin{itemize}
    \item \( \text{selected\_translators} = \{i \in T : x_i = 1\} \)
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

\section*{Mathematical Model for Translator Selection}

\subsection*{Sets}
\begin{itemize}
    \item Let \( T = \{1, 2, \ldots, N\} \) be the set of available translators.
    \item Let \( L = \{1, 2, \ldots, M\} \) be the set of required languages.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cost}_i \): Cost of hiring translator \( i \in T \).
    \item \( S_i \): Set of languages that translator \( i \) can translate (subset of \( L \)).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \) be a binary variable such that:
    \[
    x_i = 
    \begin{cases} 
    1 & \text{if translator } i \text{ is selected} \\ 
    0 & \text{otherwise} 
    \end{cases}
    \]
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of selected translators:
\[
\text{Minimize } Z = \sum_{i \in T} \text{cost}_i \cdot x_i
\]

\subsection*{Constraints}
Ensure all required languages are covered:
\[
\sum_{i \in T} x_i \cdot \mathbb{I}(j \in S_i) \geq 1 \quad \forall j \in L
\]
where \( \mathbb{I}(j \in S_i) \) is an indicator function that is 1 if language \( j \) is in the set of languages that translator \( i \) can translate, and 0 otherwise.

\subsection*{Binary Constraints}
\[
x_i \in \{0, 1\} \quad \forall i \in T
\]

\subsection*{Output}
\begin{itemize}
    \item \( \text{selected\_translators} = \{i \in T : x_i = 1\} \)
    \item \( \text{total\_cost} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction
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

translators = data['translators']
required_languages = data['required_languages']

#### Create the LP Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

#### Set of translators and costs
translator_vars = {
    t['id']: pulp.LpVariable(f"x_{t['id']}", cat='Binary') for t in translators
}

#### Objective Function: Minimize the total cost
problem += pulp.lpSum(translator_vars[t['id']] * t['cost'] for t in translators)

#### Constraints: Ensure all required languages are covered
for lang in required_languages:
    problem += pulp.lpSum(
        translator_vars[t['id']] * (1 if lang in t['languages'] else 0) 
        for t in translators
    ) >= 1

#### Solve the problem
problem.solve()

#### Output results
selected_translators = [t['id'] for t in translators if pulp.value(translator_vars[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

print(f"Selected Translators: {selected_translators} (Objective Value): <OBJ>{total_cost}</OBJ>")
```

