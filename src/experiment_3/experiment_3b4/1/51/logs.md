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
To model the given problem as a linear programming problem, let's define the variables, objective function, and constraints.

######### Variables:
- Let \( x_a \) be the number of clicks purchased (in thousands) for ad type \( a \) where \( a = 1, \ldots, A \).

######### Objective:
- Maximize the total number of unique clicks
  \[
  \text{Maximize } \sum_{a=1}^{A} \text{unique\_click}_{a} \times x_a
  \]

######### Constraints:
1. Total young age group clicks:
   \[
   \sum_{a=1}^{A} \text{young\_click}_{a} \times x_a \geq \text{goal\_young}
   \]

2. Total older age group clicks:
   \[
   \sum_{a=1}^{A} \text{old\_click}_{a} \times x_a \geq \text{goal\_old}
   \]

3. Total unique young age group clicks:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_a \geq \text{goal\_unique\_young}
   \]

4. Total unique older age group clicks:
   \[
   \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_a \geq \text{goal\_unique\_old}
   \]

5. Budget constraint:
   \[
   \sum_{a=1}^{A} \text{cost}_{a} \times x_a \leq \text{budget}
   \]

6. Maximum clicks constraint for each ad:
   \[
   0 \leq x_a \leq \text{max\_click}_{a}, \quad \text{for } a = 1, \ldots, A
   \]

The linear programming model can be described in LaTeX as follows:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_a \) be the number of clicks (in thousands) for ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } \sum_{a=1}^{A} \text{unique\_click}_{a} \times x_a
\]

\subsection*{Constraints}
\begin{align*}
& \text{Total young age group clicks:} \\
& \sum_{a=1}^{A} \text{young\_click}_{a} \times x_a \geq \text{goal\_young} \\

& \text{Total older age group clicks:} \\
& \sum_{a=1}^{A} \text{old\_click}_{a} \times x_a \geq \text{goal\_old} \\

& \text{Total unique young age group clicks:} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_a \geq \text{goal\_unique\_young} \\

& \text{Total unique older age group clicks:} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_a \geq \text{goal\_unique\_old} \\

& \text{Budget constraint:} \\
& \sum_{a=1}^{A} \text{cost}_{a} \times x_a \leq \text{budget} \\

& \text{Maximum clicks constraint for each ad:} \\
& 0 \leq x_a \leq \text{max\_click}_{a}, \quad \text{for } a = 1, \ldots, A
\end{align*}

\end{document}
``` 

This model represents the problem of selecting the best number of clicks for each ad type such that the number of unique clicks is maximized, while satisfying all the given constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_a \) be the number of clicks (in thousands) for ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } \sum_{a=1}^{A} \text{unique\_click}_{a} \times x_a
\]

\subsection*{Constraints}
\begin{align*}
& \text{Total young age group clicks:} \\
& \sum_{a=1}^{A} \text{young\_click}_{a} \times x_a \geq \text{goal\_young} \\

& \text{Total older age group clicks:} \\
& \sum_{a=1}^{A} \text{old\_click}_{a} \times x_a \geq \text{goal\_old} \\

& \text{Total unique young age group clicks:} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_a \geq \text{goal\_unique\_young} \\

& \text{Total unique older age group clicks:} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_a \geq \text{goal\_unique\_old} \\

& \text{Budget constraint:} \\
& \sum_{a=1}^{A} \text{cost}_{a} \times x_a \leq \text{budget} \\

& \text{Maximum clicks constraint for each ad:} \\
& 0 \leq x_a \leq \text{max\_click}_{a}, \quad \text{for } a = 1, \ldots, A
\end{align*}

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

#### Create a problem variable
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Integer') for a in range(len(data['unique_clicks']))]

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(len(data['unique_clicks'])))

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))) >= data['goal_young'], "Young_Age_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))) >= data['goal_old'], "Old_Age_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))) >= data['goal_unique_young'], "Unique_Young_Age_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))) >= data['goal_unique_old'], "Unique_Old_Age_Clicks"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(len(data['costs']))) <= data['budget'], "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Display the results
for var in x:
    print(f'{var.name} = {var.varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

