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
To model the given problem in Linear Programming and express it in LaTeX format, we'll define variables, constraints, and the objective function. The aim is to maximize the number of unique clicks while satisfying various constraints such as budget, goals for specific age groups, and maximum allowable clicks for each ad type.

Here is the mathematical formulation for the given problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
Maximize the total number of unique clicks, which can be expressed as:

\[
\text{Maximize } \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_{a}
\]

\textbf{Subject to:}
\begin{align*}
1. & \quad \sum_{a=1}^{A} \text{cost}_{a} \cdot \text{clicks}_{a} \leq \text{budget} \\
2. & \quad \sum_{a=1}^{A} \text{young\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_young} \\
3. & \quad \sum_{a=1}^{A} \text{old\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_old} \\
4. & \quad \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_unique\_young} \quad \text{for visitors aged 18-25} \\
5. & \quad \sum_{a=1}^{A} \left(1 - \text{unique\_click}_{a}\right) \cdot \text{clicks}_{a} \geq \text{goal\_unique\_old} \quad \text{for visitors older than 25} \\
6. & \quad \text{clicks}_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, \ldots, A \\
7. & \quad \text{clicks}_{a} \geq 0, \quad \forall a = 1, \ldots, A
\end{align*}

\textbf{Decision Variables:}
- \(\text{clicks}_{a}\): The number of clicks purchased for ad type \(a\) in thousands.

\textbf{Parameters:}
- \(\text{cost}_{a}\): Cost per 1000 clicks for ad type \(a\).
- \(\text{young\_click}_{a}\): Percentage of clicks from the 18-25 age range for ad type \(a\).
- \(\text{old\_click}_{a}\): Percentage of clicks from older visitors for ad type \(a\).
- \(\text{unique\_click}_{a}\): Percentage of unique visitors for ad type \(a\).
- \(\text{max\_click}_{a}\): Maximum allowable clicks for ad type \(a\).
- \(\text{budget}\): Total advertising budget.
- \(\text{goal\_young}\), \(\text{goal\_old}\): Goals for clicks from specific age groups.
- \(\text{goal\_unique\_young}\), \(\text{goal\_unique\_old}\): Goals for unique clicks from specific age groups.

\end{document}
```

This LaTeX code represents the linear programming model for optimizing the number of unique clicks while adhering to various constraints, including budgetary and demographic goals.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
Maximize the total number of unique clicks, which can be expressed as:

\[
\text{Maximize } \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_{a}
\]

\textbf{Subject to:}
\begin{align*}
1. & \quad \sum_{a=1}^{A} \text{cost}_{a} \cdot \text{clicks}_{a} \leq \text{budget} \\
2. & \quad \sum_{a=1}^{A} \text{young\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_young} \\
3. & \quad \sum_{a=1}^{A} \text{old\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_old} \\
4. & \quad \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot \text{clicks}_{a} \geq \text{goal\_unique\_young} \quad \text{for visitors aged 18-25} \\
5. & \quad \sum_{a=1}^{A} \left(1 - \text{unique\_click}_{a}\right) \cdot \text{clicks}_{a} \geq \text{goal\_unique\_old} \quad \text{for visitors older than 25} \\
6. & \quad \text{clicks}_{a} \leq \text{max\_click}_{a}, \quad \forall a = 1, \ldots, A \\
7. & \quad \text{clicks}_{a} \geq 0, \quad \forall a = 1, \ldots, A
\end{align*}

\textbf{Decision Variables:}
- \(\text{clicks}_{a}\): The number of clicks purchased for ad type \(a\) in thousands.

\textbf{Parameters:}
- \(\text{cost}_{a}\): Cost per 1000 clicks for ad type \(a\).
- \(\text{young\_click}_{a}\): Percentage of clicks from the 18-25 age range for ad type \(a\).
- \(\text{old\_click}_{a}\): Percentage of clicks from older visitors for ad type \(a\).
- \(\text{unique\_click}_{a}\): Percentage of unique visitors for ad type \(a\).
- \(\text{max\_click}_{a}\): Maximum allowable clicks for ad type \(a\).
- \(\text{budget}\): Total advertising budget.
- \(\text{goal\_young}\), \(\text{goal\_old}\): Goals for clicks from specific age groups.
- \(\text{goal\_unique\_young}\), \(\text{goal\_unique\_old}\): Goals for unique clicks from specific age groups.

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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
A = len(data['costs'])

#### Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

#### Problem definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)), "Total Unique Clicks"

#### Constraints
#### Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "Budget"

#### Goal for young age group
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Goal_Young"

#### Goal for old age group
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Goal_Old"

#### Goal for unique clicks for young (18-25)
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

#### Goal for unique clicks for old (above 25)
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

#### Solve the problem
problem.solve()

#### Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for a in range(A):
    print(f'Clicks for Ad Type {a+1}: {clicks[a].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

