# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Custom Tees is planning an online advertising campaign with \var{A} different ad types across two web companies.
- The company has set a goal of \var{goal_young} thousand clicks from visitors aged 18-25 and \var{goal_old} thousand clicks from visitors older than 25.
- The company has set a goal of \var{goal_unique_young} thousand unique clicks from visitors aged 18-25 and \var{goal_unique_old} thousand unique clicks from visitors older than 25.
- Ad type \var{a} has an estimated percentage of \var{young_click_{a}} clicks from the 18-25 age range.
- Ad type \var{a} has an estimated percentage of \var{old_click_{a}} clicks from older visitors.
- Ad type \var{a} has a cost of \var{cost_{a}} per 1000 clicks.
- Ad type \var{a} has a maximum allowable clicks of \var{max_click_{a}} in thousands.
- The estimated percentage of unique visitors for each ad type \var{a} is \var{unique_click_{a}}.
- The company has an advertising budget of $\var{budget}

INPUT FORMAT: 

{
    "goal_young": goal_young,
    "goal_old": goal_old,
    "goal_unique_young": goal_unique_young,
    "goal_unique_old": goal_unique_old,
    "young_clicks": [young_click_{a} for a in 1,...,A],
    "old_clicks": [old_click_{a} for a in 1,...,A],
    "costs": [cost_{a} for a in 1,...,A],
    "max_clicks": [max_click_{a} for a in 1,...,A],
    "unique_clicks": [unique_click_{a} for a in 1,...,A],
    "budget": budget
}

OBJECTIVE: How many clicks from each ad type should Custom Tees purchase to maximize the number of unique clicks within the budget?

OUTPUT INFO:

- the number of clicks purchased for each ad type is \var{clicks_{a}} in thousands.
- \var{total_unique_clicks} represents the total number of unique clicks.

OUTPUT FORMAT:

{
    "clicks": [click_{a} for a in 1, ..., A],
    "total_unique_clicks": total_unique_clicks
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \) be the number of different ad types.
    \item \( \text{goal\_young} \) is the goal of clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_old} \) is the goal of clicks from visitors older than 25 (in thousands).
    \item \( \text{goal\_unique\_young} \) is the goal of unique clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_unique\_old} \) is the goal of unique clicks from visitors older than 25 (in thousands).
    \item \( \text{young\_click}_{a} \) is the estimated percentage of clicks from the 18-25 age range for ad type \( a \).
    \item \( \text{old\_click}_{a} \) is the estimated percentage of clicks from visitors older than 25 for ad type \( a \).
    \item \( \text{cost}_{a} \) is the cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_{a} \) is the maximum allowable clicks in thousands for ad type \( a \).
    \item \( \text{unique\_click}_{a} \) is the estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \) is the total advertising budget.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{a} \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a}
\]

\subsection*{Constraints}
1. **Click Goals from Age Groups**:
    \[
    \sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_{a} \geq \text{goal\_young}
    \]
    \[
    \sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_{a} \geq \text{goal\_old}
    \]

2. **Unique Click Goals**:
    \[
    \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_young} + \text{goal\_unique\_old}
    \]

3. **Maximum Clicks**:
    \[
    x_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, 2, \ldots, A
    \]

4. **Budget Constraint**:
    \[
    \sum_{a=1}^{A} \text{cost}_{a} \cdot x_{a} \leq \text{budget}
    \]

5. **Non-negativity**:
    \[
    x_{a} \geq 0, \quad \forall a = 1, 2, \ldots, A
    \]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The optimal number of clicks purchased for each ad type: \( x_{a} \) for \( a = 1, \ldots, A \).
    \item The total number of unique clicks obtained: \( Z \).
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

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \) be the number of different ad types.
    \item \( \text{goal\_young} \) is the goal of clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_old} \) is the goal of clicks from visitors older than 25 (in thousands).
    \item \( \text{goal\_unique\_young} \) is the goal of unique clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_unique\_old} \) is the goal of unique clicks from visitors older than 25 (in thousands).
    \item \( \text{young\_click}_{a} \) is the estimated percentage of clicks from the 18-25 age range for ad type \( a \).
    \item \( \text{old\_click}_{a} \) is the estimated percentage of clicks from visitors older than 25 for ad type \( a \).
    \item \( \text{cost}_{a} \) is the cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_{a} \) is the maximum allowable clicks in thousands for ad type \( a \).
    \item \( \text{unique\_click}_{a} \) is the estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \) is the total advertising budget.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{a} \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a}
\]

\subsection*{Constraints}
1. **Click Goals from Age Groups**:
    \[
    \sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_{a} \geq \text{goal\_young}
    \]
    \[
    \sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_{a} \geq \text{goal\_old}
    \]

2. **Unique Click Goals**:
    \[
    \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_young} + \text{goal\_unique\_old}
    \]

3. **Maximum Clicks**:
    \[
    x_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, 2, \ldots, A
    \]

4. **Budget Constraint**:
    \[
    \sum_{a=1}^{A} \text{cost}_{a} \cdot x_{a} \leq \text{budget}
    \]

5. **Non-negativity**:
    \[
    x_{a} \geq 0, \quad \forall a = 1, 2, \ldots, A
    \]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The optimal number of clicks purchased for each ad type: \( x_{a} \) for \( a = 1, \ldots, A \).
    \item The total number of unique clicks obtained: \( Z \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

#### Parameters
A = len(data['young_clicks'])  #### Number of different ad types
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique = data['goal_unique_young'] + data['goal_unique_old']
max_clicks = data['max_clicks']
costs = data['costs']
budget = data['budget']

#### Decision Variables
x = pulp.LpVariable.dicts('x', range(A), lowBound=0, upBound=None, cat='Continuous')

#### Problem definition
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total Unique Clicks"

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= goal_young, "Young Age Click Goals"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= goal_old, "Old Age Click Goals"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= goal_unique, "Unique Click Goals"

for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max Clicks for Ad Type {a+1}"

problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget Constraint"

#### Solve the problem
problem.solve()

#### Output the results
for a in range(A):
    print(f'Clicks purchased for ad type {a + 1}: {x[a].varValue} (in thousands)')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

