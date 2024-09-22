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
To model this problem, we'll define the Linear Programming (LP) formulation in LaTeX. The objective is to maximize the total number of unique clicks within the given budget and other constraints.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising}

\subsection*{Decision Variables}
Let \( x_a \) represent the number of clicks (in thousands) purchased for ad type \( a \) where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
We aim to maximize the total number of unique clicks:

\[
\max \sum_{a=1}^{A} \text{unique\_click}_{a} \times x_{a}
\]

\subsection*{Constraints}

1. Budget Constraint:
   \[
   \sum_{a=1}^{A} \text{cost}_{a} \times x_{a} \leq \text{budget}
   \]

2. Young Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{young\_click}_{a} \times x_{a} \geq \text{goal\_young}
   \]

3. Older Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{old\_click}_{a} \times x_{a} \geq \text{goal\_old}
   \]

4. Young Unique Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_{a} \geq \text{goal\_unique\_young}
   \]

5. Older Unique Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_{a} \geq \text{goal\_unique\_old}
   \]

6. Maximum Clicks Constraint for each ad type:
   \[
   0 \leq x_{a} \leq \text{max\_click}_{a} \quad \text{for all } a = 1, 2, \ldots, A
   \]

\subsection*{Summary}
The solution to this linear programming problem provides the number of clicks \( x_a \) to purchase for each ad type in order to maximize unique clicks, while satisfying the budget and demographic goals.

\end{document}
```

This LaTeX document outlines the decision variables, objective function, and constraints required to solve the problem using linear programming.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising}

\subsection*{Decision Variables}
Let \( x_a \) represent the number of clicks (in thousands) purchased for ad type \( a \) where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
We aim to maximize the total number of unique clicks:

\[
\max \sum_{a=1}^{A} \text{unique\_click}_{a} \times x_{a}
\]

\subsection*{Constraints}

1. Budget Constraint:
   \[
   \sum_{a=1}^{A} \text{cost}_{a} \times x_{a} \leq \text{budget}
   \]

2. Young Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{young\_click}_{a} \times x_{a} \geq \text{goal\_young}
   \]

3. Older Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{old\_click}_{a} \times x_{a} \geq \text{goal\_old}
   \]

4. Young Unique Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_{a} \geq \text{goal\_unique\_young}
   \]

5. Older Unique Visitors Clicks Goal:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_{a} \geq \text{goal\_unique\_old}
   \]

6. Maximum Clicks Constraint for each ad type:
   \[
   0 \leq x_{a} \leq \text{max\_click}_{a} \quad \text{for all } a = 1, 2, \ldots, A
   \]

\subsection*{Summary}
The solution to this linear programming problem provides the number of clicks \( x_a \) to purchase for each ad type in order to maximize unique clicks, while satisfying the budget and demographic goals.

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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
A = len(data['unique_clicks'])

#### Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

#### Objective function
objective = pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A))
problem += objective

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

#### Young Visitors Clicks Goal
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Goal"

#### Older Visitors Clicks Goal
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Goal"

#### Young Unique Visitors Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Young_Unique_Clicks_Goal"

#### Older Unique Visitors Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Old_Unique_Clicks_Goal"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

