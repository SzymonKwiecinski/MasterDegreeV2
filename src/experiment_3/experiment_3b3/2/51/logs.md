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

\section*{Linear Programming Model for Online Advertising Campaign}

\subsection*{Parameters}
\begin{align*}
& \text{Let } A \text{ be the number of ad types,} \\
& \text{goal\_young: the goal of clicks from visitors aged 18-25 (in thousands),} \\
& \text{goal\_old: the goal of clicks from visitors older than 25 (in thousands),} \\
& \text{goal\_unique\_young: the goal of unique clicks from visitors aged 18-25 (in thousands),} \\
& \text{goal\_unique\_old: the goal of unique clicks from visitors older than 25 (in thousands),} \\
& \text{young\_clicks}_a: \text{percentage of clicks from the 18-25 age range for ad type } a, \\
& \text{old\_clicks}_a: \text{percentage of clicks from older visitors for ad type } a, \\
& \text{cost}_a: \text{cost per 1000 clicks for ad type } a, \\
& \text{max\_clicks}_a: \text{maximum allowable clicks for ad type } a \text{ (in thousands),} \\
& \text{unique\_clicks}_a: \text{estimated percentage of unique visitors for ad type } a, \\
& \text{budget: total advertising budget.}
\end{align*}

\subsection*{Decision Variables}
Let \( \text{clicks}_a \) be the number of clicks purchased for ad type \( a \) (in thousands).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a
\]

\subsection*{Constraints}
1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_young}
\]
2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_old}
\]
3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_unique\_young}
\]
4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_unique\_old}
\]
5. Budget constraint:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot \text{clicks}_a \leq \text{budget}
\]
6. Maximum allowable clicks for each ad type:
\[
\text{clicks}_a \leq \text{max\_clicks}_a, \quad \forall a \in \{1, \ldots, A\}
\]
7. Non-negativity:
\[
\text{clicks}_a \geq 0, \quad \forall a \in \{1, \ldots, A\}
\]

\subsection*{Output Variables}
The outputs will be:
\begin{itemize}
    \item \( \text{clicks} = [\text{clicks}_1, \text{clicks}_2, \ldots, \text{clicks}_A] \)
    \item \( \text{total\_unique\_clicks} = Z \)
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

\section*{Linear Programming Model for Online Advertising Campaign}

\subsection*{Parameters}
\begin{align*}
& \text{Let } A \text{ be the number of ad types,} \\
& \text{goal\_young: the goal of clicks from visitors aged 18-25 (in thousands),} \\
& \text{goal\_old: the goal of clicks from visitors older than 25 (in thousands),} \\
& \text{goal\_unique\_young: the goal of unique clicks from visitors aged 18-25 (in thousands),} \\
& \text{goal\_unique\_old: the goal of unique clicks from visitors older than 25 (in thousands),} \\
& \text{young\_clicks}_a: \text{percentage of clicks from the 18-25 age range for ad type } a, \\
& \text{old\_clicks}_a: \text{percentage of clicks from older visitors for ad type } a, \\
& \text{cost}_a: \text{cost per 1000 clicks for ad type } a, \\
& \text{max\_clicks}_a: \text{maximum allowable clicks for ad type } a \text{ (in thousands),} \\
& \text{unique\_clicks}_a: \text{estimated percentage of unique visitors for ad type } a, \\
& \text{budget: total advertising budget.}
\end{align*}

\subsection*{Decision Variables}
Let \( \text{clicks}_a \) be the number of clicks purchased for ad type \( a \) (in thousands).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a
\]

\subsection*{Constraints}
1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_young}
\]
2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_old}
\]
3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_unique\_young}
\]
4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{unique\_clicks}_a \cdot \text{clicks}_a \geq \text{goal\_unique\_old}
\]
5. Budget constraint:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot \text{clicks}_a \leq \text{budget}
\]
6. Maximum allowable clicks for each ad type:
\[
\text{clicks}_a \leq \text{max\_clicks}_a, \quad \forall a \in \{1, \ldots, A\}
\]
7. Non-negativity:
\[
\text{clicks}_a \geq 0, \quad \forall a \in \{1, \ldots, A\}
\]

\subsection*{Output Variables}
The outputs will be:
\begin{itemize}
    \item \( \text{clicks} = [\text{clicks}_1, \text{clicks}_2, \ldots, \text{clicks}_A] \)
    \item \( \text{total\_unique\_clicks} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Number of ad types
A = len(data['young_clicks'])

#### Create Linear Programming problem
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMaximize)

#### Decision variables
clicks = [pulp.LpVariable(f'clicks_{a+1}', lowBound=0, cat='Continuous') for a in range(A)]

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

#### Constraints
#### 1. Clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

#### 2. Clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

#### 3. Unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']

#### 4. Unique clicks from visitors older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']

#### 5. Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

#### 6. Maximum allowable clicks for each ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

#### Solve the problem
problem.solve()

#### Print the results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks: {clicks_result}')
print(f'Total Unique Clicks (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')
```

