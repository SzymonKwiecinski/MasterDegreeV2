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
To solve this Linear Programming problem, we will minimize the total cost of the advertising campaign while meeting the constraints related to clicks from different age groups, unique clicks, and maximum allowable clicks for each ad type. 

Let's define the variables and constraints for the LP problem:

1. **Decision Variables**:
   - \( x_a \): Number of clicks (in thousands) purchased for ad type \( a \), for \( a = 1, \ldots, A \).

2. **Objective Function**:
   - Minimize the total cost of the ad campaign: \(\sum_{a=1}^{A} \text{cost}_a \cdot x_a\).

3. **Constraints**:
   - Total clicks from visitors aged 18-25 should be at least \( \text{goal\_young} \) thousand: \(\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}\).
   - Total clicks from visitors older than 25 should be at least \( \text{goal\_old} \) thousand: \(\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}\).
   - Total unique clicks from visitors aged 18-25 should be at least \( \text{goal\_unique\_young} \) thousand: \(\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{young\_click}_a \cdot x_a \geq \text{goal\_unique\_young}\).
   - Total unique clicks from visitors older than 25 should be at least \( \text{goal\_unique\_old} \) thousand: \(\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{old\_click}_a \cdot x_a \geq \text{goal\_unique\_old}\).
   - The number of clicks for each ad type cannot exceed the maximum allowable clicks: \( 0 \leq x_a \leq \text{max\_click}_a \) for \( a = 1, \ldots, A \).

Here is the mathematical formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{align*}
x_a & : \text{Number of clicks purchased for ad type } a \text{ (in thousands).}
\end{align*}

\textbf{Objective:}
\begin{align*}
\text{Minimize } & \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\end{align*}

\textbf{Subject to:}
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a & \geq \text{goal\_young}, \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a & \geq \text{goal\_old}, \\
\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{young\_click}_a \cdot x_a & \geq \text{goal\_unique\_young}, \\
\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{old\_click}_a \cdot x_a & \geq \text{goal\_unique\_old}, \\
0 \leq x_a & \leq \text{max\_click}_a, \quad \forall a \in \{1, \ldots, A\}.
\end{align*}

\end{document}
```

This is a typical linear programming problem where the decision variables, objective function, and constraints are all linear. The intention is to purchase the optimal number of clicks per ad type to minimize the total campaign cost while satisfying all the click goals and constraints.

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

\textbf{Decision Variables:}
\begin{align*}
x_a & : \text{Number of clicks purchased for ad type } a \text{ (in thousands).}
\end{align*}

\textbf{Objective:}
\begin{align*}
\text{Minimize } & \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\end{align*}

\textbf{Subject to:}
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a & \geq \text{goal\_young}, \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a & \geq \text{goal\_old}, \\
\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{young\_click}_a \cdot x_a & \geq \text{goal\_unique\_young}, \\
\sum_{a=1}^{A} \text{unique\_click}_a \cdot \text{old\_click}_a \cdot x_a & \geq \text{goal\_unique\_old}, \\
0 \leq x_a & \leq \text{max\_click}_a, \quad \forall a \in \{1, \ldots, A\}.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


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
    'unique_clicks': [40, 75, 90]
}

#### Decision Variables
num_ads = len(data['costs'])
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(num_ads)]

#### Problem
problem = pulp.LpProblem("Minimize_Advertising_Costs", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum([data['costs'][a] * x[a] for a in range(num_ads)])

#### Constraints
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_old']
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_unique_old']

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

