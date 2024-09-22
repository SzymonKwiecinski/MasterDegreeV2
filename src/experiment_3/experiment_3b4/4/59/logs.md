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
To solve this problem, we'll formulate it as a Mixed Integer Linear Programming (MILP) problem. We'll define binary decision variables for each translator to decide whether they are included in the team or not. The objective function will minimize the total cost while ensuring that all required languages are covered by the selected translators.

Let's define the mathematical model for the given problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\textbf{Sets:}
\begin{align*}
  & T = \{1, 2, \ldots, N\} \quad \text{(set of translators)} \\
  & L = \{1, 2, \ldots, M\} \quad \text{(set of required languages)}
\end{align*}

\textbf{Parameters:}
\begin{align*}
  & \text{cost}_i \quad \text{Cost of hiring translator } i, \quad \forall i \in T \\
  & A_{ij} = 
  \begin{cases} 
    1, & \text{if translator } i \text{ can translate language } j \\ 
    0, & \text{otherwise}
  \end{cases}, \quad \forall i \in T, j \in L
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
  & x_i \in \{0, 1\}, \quad \text{Binary variable indicating whether translator } i \text{ is selected}, \quad \forall i \in T
\end{align*}

\textbf{Objective Function:}
\begin{align*}
  & \min \sum_{i \in T} \text{cost}_i \cdot x_i
\end{align*}

\textbf{Constraints:}
\begin{align*}
  & \sum_{i \in T} A_{ij} \cdot x_i \geq 1, \quad \forall j \in L \quad \text{(ensure each required language is covered)}
\end{align*}

The above formulation ensures that we pick the minimum cost set of translators such that all required languages are covered.

\end{document}
```

This MILP formulation includes:
- Decision variables \( x_i \) indicating whether a translator \( i \) is selected.
- An objective function to minimize the total cost of selected translators.
- Constraints to ensure that each required language is covered by at least one selected translator.

This approach provides a structured way to select translators while minimizing the cost and ensuring language coverage as required for the summer Olympics.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\textbf{Sets:}
\begin{align*}
  & T = \{1, 2, \ldots, N\} \quad \text{(set of translators)} \\
  & L = \{1, 2, \ldots, M\} \quad \text{(set of required languages)}
\end{align*}

\textbf{Parameters:}
\begin{align*}
  & \text{cost}_i \quad \text{Cost of hiring translator } i, \quad \forall i \in T \\
  & A_{ij} = 
  \begin{cases} 
    1, & \text{if translator } i \text{ can translate language } j \\ 
    0, & \text{otherwise}
  \end{cases}, \quad \forall i \in T, j \in L
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
  & x_i \in \{0, 1\}, \quad \text{Binary variable indicating whether translator } i \text{ is selected}, \quad \forall i \in T
\end{align*}

\textbf{Objective Function:}
\begin{align*}
  & \min \sum_{i \in T} \text{cost}_i \cdot x_i
\end{align*}

\textbf{Constraints:}
\begin{align*}
  & \sum_{i \in T} A_{ij} \cdot x_i \geq 1, \quad \forall j \in L \quad \text{(ensure each required language is covered)}
\end{align*}

The above formulation ensures that we pick the minimum cost set of translators such that all required languages are covered.

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
        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

#### Initialize the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

#### Sets
translators = data['translators']
required_languages = data['required_languages']

#### Decision variables
x = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary') for translator in translators}

#### Objective function
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in translators)

#### Constraints
for language in required_languages:
    problem += pulp.lpSum(x[translator['id']] for translator in translators if language in translator['languages']) >= 1

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

