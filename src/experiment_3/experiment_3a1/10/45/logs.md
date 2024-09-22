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

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Parameters}
\begin{align*}
& \text{let } A \text{ be the number of ad types} \\
& \text{let } goal\_young \text{ be the target clicks from visitors aged 18-25 (in thousands)} \\
& \text{let } goal\_old \text{ be the target clicks from visitors older than 25 (in thousands)} \\
& \text{let } goal\_unique\_young \text{ be the target unique clicks from visitors aged 18-25 (in thousands)} \\
& \text{let } goal\_unique\_old \text{ be the target unique clicks from visitors older than 25 (in thousands)} \\
& \text{let } young\_click_{a} \text{ be the percentage of clicks from age 18-25 for ad type } a \\
& \text{let } old\_click_{a} \text{ be the percentage of clicks from age >25 for ad type } a \\
& \text{let } cost_{a} \text{ be the cost per 1000 clicks for ad type } a \\
& \text{let } max\_click_{a} \text{ be the maximum allowable clicks for ad type } a \\
& \text{let } unique\_click_{a} \text{ be the estimated percentage of unique visitors for ad type } a 
\end{align*}

\subsection*{Decision Variables}
Let \( clicks_a \) represent the number of clicks purchased for ad type \( a \) (in thousands), for \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } total\_cost = \sum_{a=1}^{A} cost_a \cdot clicks_a
\]

\subsection*{Constraints}
1. Total clicks from young visitors:
\[
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_a \geq goal\_young
\]
2. Total clicks from older visitors:
\[
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_a \geq goal\_old
\]
3. Total unique clicks from young visitors:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_a \geq goal\_unique\_young
\]
4. Total unique clicks from older visitors:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_a \geq goal\_unique\_old
\]
5. Maximum clicks for each ad type:
\[
clicks_a \leq max\_click_a \quad \forall a = 1, \ldots, A
\]
6. Non-negativity constraints:
\[
clicks_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The solution will provide:
\begin{align*}
& clicks_a \text{ for } a = 1, \ldots, A \text{ (in thousands)} \\
& total\_cost \text{ representing the total cost of the ad campaign}
\end{align*}

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
\begin{align*}
& \text{let } A \text{ be the number of ad types} \\
& \text{let } goal\_young \text{ be the target clicks from visitors aged 18-25 (in thousands)} \\
& \text{let } goal\_old \text{ be the target clicks from visitors older than 25 (in thousands)} \\
& \text{let } goal\_unique\_young \text{ be the target unique clicks from visitors aged 18-25 (in thousands)} \\
& \text{let } goal\_unique\_old \text{ be the target unique clicks from visitors older than 25 (in thousands)} \\
& \text{let } young\_click_{a} \text{ be the percentage of clicks from age 18-25 for ad type } a \\
& \text{let } old\_click_{a} \text{ be the percentage of clicks from age >25 for ad type } a \\
& \text{let } cost_{a} \text{ be the cost per 1000 clicks for ad type } a \\
& \text{let } max\_click_{a} \text{ be the maximum allowable clicks for ad type } a \\
& \text{let } unique\_click_{a} \text{ be the estimated percentage of unique visitors for ad type } a 
\end{align*}

\subsection*{Decision Variables}
Let \( clicks_a \) represent the number of clicks purchased for ad type \( a \) (in thousands), for \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } total\_cost = \sum_{a=1}^{A} cost_a \cdot clicks_a
\]

\subsection*{Constraints}
1. Total clicks from young visitors:
\[
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_a \geq goal\_young
\]
2. Total clicks from older visitors:
\[
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_a \geq goal\_old
\]
3. Total unique clicks from young visitors:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_a \geq goal\_unique\_young
\]
4. Total unique clicks from older visitors:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_a \geq goal\_unique\_old
\]
5. Maximum clicks for each ad type:
\[
clicks_a \leq max\_click_a \quad \forall a = 1, \ldots, A
\]
6. Non-negativity constraints:
\[
clicks_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\subsection*{Output}
The solution will provide:
\begin{align*}
& clicks_a \text{ for } a = 1, \ldots, A \text{ (in thousands)} \\
& total\_cost \text{ representing the total cost of the ad campaign}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Here's the Python script using the Pulp library to solve the Linear Programming model for the Custom Tees Advertising Campaign based on the provided mathematical model and data:

```python
import pulp
import json

#### Input data
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}")

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
A = len(costs)  #### Number of ad types

#### Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

#### Problem Definition
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Visitor_Clicks"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Visitor_Clicks"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Visitor_Clicks"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Visitor_Clicks"

for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_{a}"

#### Solve the problem
problem.solve()

#### Output
for a in range(A):
    print(f'Clicks for ad type {a + 1} (in thousands): {clicks[a].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
``` 

This code defines the linear programming model based on your specifications, sets up the objective function and constraints, solves the problem, and finally prints the results. Make sure to run this script in an environment where the Pulp library is available.

