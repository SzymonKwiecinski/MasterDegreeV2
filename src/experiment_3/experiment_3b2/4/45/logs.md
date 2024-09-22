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
To solve this problem using Linear Programming, we need to formulate it in terms of objective function and constraints. The goal is to minimize the total cost while satisfying the constraints on the number of clicks from different age groups as well as unique clicks.

Firstly, let's define the decision variables:
- \( x_a \): the number of clicks (in thousands) purchased for ad type \( a \)

The objective function is to minimize the total cost of the ad campaign, which can be expressed as:
\[
\text{Minimize} \quad \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

Subject to the following constraints:
1. Total clicks from visitors aged 18-25 should be at least \(\text{goal\_young}\):
   \[
   \sum_{a=1}^{A} \text{young\_clicks}_a \cdot x_a \geq \text{goal\_young}
   \]

2. Total clicks from visitors older than 25 should be at least \(\text{goal\_old}\):
   \[
   \sum_{a=1}^{A} \text{old\_clicks}_a \cdot x_a \geq \text{goal\_old}
   \]

3. Total unique clicks from visitors aged 18-25 should be at least \(\text{goal\_unique\_young}\):
   \[
   \sum_{a=1}^{A} \text{young\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_young}
   \]

4. Total unique clicks from visitors older than 25 should be at least \(\text{goal\_unique\_old}\):
   \[
   \sum_{a=1}^{A} \text{old\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_old}
   \]

5. Maximum allowable clicks constraint for each ad type:
   \[
   0 \leq x_a \leq \text{max\_clicks}_a \quad \text{for each } a = 1, \ldots, A
   \]

Now, let's put this into a LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

\text{Objective:}
\begin{align*}
\text{Minimize} \quad & \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\end{align*}

\text{Subject to:}
\begin{align*}
& \sum_{a=1}^{A} \text{young\_clicks}_a \cdot x_a \geq \text{goal\_young} & \text{(Clicks from 18-25)} \\
& \sum_{a=1}^{A} \text{old\_clicks}_a \cdot x_a \geq \text{goal\_old} & \text{(Clicks from 25+)} \\
& \sum_{a=1}^{A} \text{young\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_young} & \text{(Unique clicks from 18-25)} \\
& \sum_{a=1}^{A} \text{old\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_old} & \text{(Unique clicks from 25+)} \\
& 0 \leq x_a \leq \text{max\_clicks}_a & \text{for each } a = 1, \ldots, A
\end{align*}

\end{document}
```

This LaTeX code models the linear programming problem that Custom Tees needs to solve to optimize their ad campaign costs while meeting their click and demographic goals.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation}

\text{Objective:}
\begin{align*}
\text{Minimize} \quad & \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\end{align*}

\text{Subject to:}
\begin{align*}
& \sum_{a=1}^{A} \text{young\_clicks}_a \cdot x_a \geq \text{goal\_young} & \text{(Clicks from 18-25)} \\
& \sum_{a=1}^{A} \text{old\_clicks}_a \cdot x_a \geq \text{goal\_old} & \text{(Clicks from 25+)} \\
& \sum_{a=1}^{A} \text{young\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_young} & \text{(Unique clicks from 18-25)} \\
& \sum_{a=1}^{A} \text{old\_clicks}_a \cdot \text{unique\_clicks}_a \cdot x_a \geq \text{goal\_unique\_old} & \text{(Unique clicks from 25+)} \\
& 0 \leq x_a \leq \text{max\_clicks}_a & \text{for each } a = 1, \ldots, A
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


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
    'unique_clicks': [40, 75, 90]
}

#### Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

#### Number of alternatives
A = len(data['costs'])

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total Cost"

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young Clicks Goal"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old Clicks Goal"
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique Young Clicks Goal"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique Old Clicks Goal"

#### Max clicks constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max Clicks {a}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

