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
    \item Let \( \text{goal\_young} \) be the target number of clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_old} \) be the target number of clicks from visitors older than 25 (in thousands).
    \item Let \( \text{goal\_unique\_young} \) be the target number of unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_unique\_old} \) be the target number of unique clicks from visitors older than 25 (in thousands).
    \item Let \( \text{young\_click}_{a} \) be the estimated percentage of clicks from the 18-25 age range for ad type \( a \).
    \item Let \( \text{old\_click}_{a} \) be the estimated percentage of clicks from older visitors for ad type \( a \).
    \item Let \( \text{cost}_{a} \) be the cost per 1000 clicks for ad type \( a \).
    \item Let \( \text{max\_click}_{a} \) be the maximum allowable clicks (in thousands) for ad type \( a \).
    \item Let \( \text{unique\_click}_{a} \) be the estimated percentage of unique visitors for each ad type \( a \).
    \item Let \( \text{budget} \) be the total advertising budget.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{clicks}_{a} \) be the number of clicks purchased for ad type \( a \) (in thousands).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a
\]

\subsection*{Constraints}
1. Total budget constraint:
\[
\sum_{a=1}^{A} \text{cost}_{a} \cdot \text{clicks}_a \leq \text{budget}
\]
2. Young clicks constraint:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_young}
\]
3. Old clicks constraint:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_old}
\]
4. Unique clicks constraints for the young demographic:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_unique\_young}
\]
5. Unique clicks constraints for the old demographic:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_unique\_old}
\]
6. Maximum clicks constraint:
\[
\text{clicks}_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, \ldots, A
\]
7. Non-negativity constraints:
\[
\text{clicks}_{a} \geq 0, \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( \text{clicks}_{a} \) (in thousands).
    \item The total number of unique clicks: \( \text{total\_unique\_clicks} \).
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
    \item Let \( \text{goal\_young} \) be the target number of clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_old} \) be the target number of clicks from visitors older than 25 (in thousands).
    \item Let \( \text{goal\_unique\_young} \) be the target number of unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_unique\_old} \) be the target number of unique clicks from visitors older than 25 (in thousands).
    \item Let \( \text{young\_click}_{a} \) be the estimated percentage of clicks from the 18-25 age range for ad type \( a \).
    \item Let \( \text{old\_click}_{a} \) be the estimated percentage of clicks from older visitors for ad type \( a \).
    \item Let \( \text{cost}_{a} \) be the cost per 1000 clicks for ad type \( a \).
    \item Let \( \text{max\_click}_{a} \) be the maximum allowable clicks (in thousands) for ad type \( a \).
    \item Let \( \text{unique\_click}_{a} \) be the estimated percentage of unique visitors for each ad type \( a \).
    \item Let \( \text{budget} \) be the total advertising budget.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{clicks}_{a} \) be the number of clicks purchased for ad type \( a \) (in thousands).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a
\]

\subsection*{Constraints}
1. Total budget constraint:
\[
\sum_{a=1}^{A} \text{cost}_{a} \cdot \text{clicks}_a \leq \text{budget}
\]
2. Young clicks constraint:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_young}
\]
3. Old clicks constraint:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_old}
\]
4. Unique clicks constraints for the young demographic:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_unique\_young}
\]
5. Unique clicks constraints for the old demographic:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_a \geq \text{goal\_unique\_old}
\]
6. Maximum clicks constraint:
\[
\text{clicks}_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, \ldots, A
\]
7. Non-negativity constraints:
\[
\text{clicks}_{a} \geq 0, \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( \text{clicks}_{a} \) (in thousands).
    \item The total number of unique clicks: \( \text{total\_unique\_clicks} \).
\end{itemize}
\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

#### Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

#### Number of ad types
A = len(costs)

#### Create the model
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

#### Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
#### Total budget constraint
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

#### Young clicks constraint
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"

#### Old clicks constraint
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"

#### Unique clicks constraints for the young demographic
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Clicks_Young_Constraint"

#### Unique clicks constraints for the old demographic
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Clicks_Old_Constraint"

#### Maximum clicks constraint
for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}"

#### Solve the problem
problem.solve()

#### Output the results
for a in range(A):
    print(f'Clicks purchased for ad type {a+1}: {clicks[a].varValue} (in thousands)')

total_unique_clicks = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')
```

