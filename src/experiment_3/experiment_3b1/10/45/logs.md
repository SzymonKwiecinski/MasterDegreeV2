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
    "unique_clicks": [unique_click_{a} for a in 1,...,A]
}

OBJECTIVE: How many clicks from each ad type should Custom Tees purchase to minimize cost?

OUTPUT INFO:

- the number of clicks purchased for each ad type is \var{clicks_{a}} in thousands.
- \var{total_cost} represents the total cost of the ad campaign.

OUTPUT FORMAT:

{
    "clicks": [click_{a} for a in 1, ..., A],
    "total_cost": total_cost
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \): Number of different ad types.
    \item Let \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_old} \): Target clicks from visitors older than 25 (in thousands).
    \item Let \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (in thousands).
    \item Let \( \text{young\_click}_{a} \): Percentage of clicks from 18-25 age range for ad type \( a \).
    \item Let \( \text{old\_click}_{a} \): Percentage of clicks from visitors older than 25 for ad type \( a \).
    \item Let \( \text{cost}_{a} \): Cost of ad type \( a \) per 1000 clicks.
    \item Let \( \text{max\_click}_{a} \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item Let \( \text{unique\_click}_{a} \): Estimated percentage of unique visitors for ad type \( a \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_a \): Number of clicks purchased for ad type \( a \) (in thousands) for \( a = 1, \ldots, A \).

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{a=1}^{A} \text{cost}_{a} \cdot x_{a}
\]

\subsection*{Constraints}
1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_{a} \geq \text{goal\_young}
\]

2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_{a} \geq \text{goal\_old}
\]

3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_young}
\]

4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
x_{a} \leq \text{max\_click}_{a} \quad \forall a = 1, \ldots, A
\]

6. Non-negativity constraints:
\[
x_{a} \geq 0 \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item Clicks purchased for each ad type: \( \{ x_{a} \}_{a=1}^{A} \) in thousands.
    \item Total cost of the ad campaign: \( Z \).
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

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \): Number of different ad types.
    \item Let \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_old} \): Target clicks from visitors older than 25 (in thousands).
    \item Let \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (in thousands).
    \item Let \( \text{young\_click}_{a} \): Percentage of clicks from 18-25 age range for ad type \( a \).
    \item Let \( \text{old\_click}_{a} \): Percentage of clicks from visitors older than 25 for ad type \( a \).
    \item Let \( \text{cost}_{a} \): Cost of ad type \( a \) per 1000 clicks.
    \item Let \( \text{max\_click}_{a} \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item Let \( \text{unique\_click}_{a} \): Estimated percentage of unique visitors for ad type \( a \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_a \): Number of clicks purchased for ad type \( a \) (in thousands) for \( a = 1, \ldots, A \).

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{a=1}^{A} \text{cost}_{a} \cdot x_{a}
\]

\subsection*{Constraints}
1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_{a} \geq \text{goal\_young}
\]

2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_{a} \geq \text{goal\_old}
\]

3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_young}
\]

4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_{a} \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
x_{a} \leq \text{max\_click}_{a} \quad \forall a = 1, \ldots, A
\]

6. Non-negativity constraints:
\[
x_{a} \geq 0 \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item Clicks purchased for each ad type: \( \{ x_{a} \}_{a=1}^{A} \) in thousands.
    \item Total cost of the ad campaign: \( Z \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data_json = '{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}'
data = json.loads(data_json)

#### Parameters
A = len(data['young_clicks'])
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

#### Create the linear programming problem
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

#### Objective function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

#### Constraints
problem += (pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint")
problem += (pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint")
for a in range(A):
    problem += (x[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}")

#### Solve the problem
problem.solve()

#### Output the results
clicks_purchased = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks purchased for each ad type (in thousands): {clicks_purchased}')
print(f'Total cost of the ad campaign (Objective Value): <OBJ>{total_cost}</OBJ>')
```

