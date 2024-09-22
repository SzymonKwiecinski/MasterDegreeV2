# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Wild Sports produces \var{M} different products using \var{N} different raw materials.
- The company has \var{available_{i}} of raw material \var{i} available.
- Product \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Product \var{j} has a selling price of \var{price_j} per unit.
- Product \var{j} has a production cost of \var{cost_j} per unit produced.
- Product \var{j} has a forecasted maximum demand of \var{demand_j} for the month.

INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}

OBJECTIVE: How many of each product should the sports produce in order to maximize its profit for the month?

OUTPUT INFO:

- the amount of each product produced \var{amount_{j}}.
- \var{total_profit} shows the total profit of the company for the month.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Variables}
Let \( x_j \) be the amount produced of product \( j \) for \( j = 1, \ldots, M \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which can be expressed as:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\subsection*{Constraints}
1. **Raw Material Constraints**:
   For each raw material \( i \) (where \( i = 1, \ldots, N \)):
   \[
   \sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i
   \]

2. **Demand Constraints**:
   For each product \( j \):
   \[
   x_j \leq demand_j
   \]

3. **Non-negativity Constraints**:
   For each product \( j \):
   \[
   x_j \geq 0
   \]

\subsection*{Input Format}
The input format for the model is as follows:
\begin{verbatim}
{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}
\end{verbatim}

\subsection*{Output Format}
The output format of the solution will be:
\begin{verbatim}
{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}
\end{verbatim}

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

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Variables}
Let \( x_j \) be the amount produced of product \( j \) for \( j = 1, \ldots, M \).

\subsection*{Objective Function}
The objective is to maximize the total profit, which can be expressed as:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\subsection*{Constraints}
1. **Raw Material Constraints**:
   For each raw material \( i \) (where \( i = 1, \ldots, N \)):
   \[
   \sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i
   \]

2. **Demand Constraints**:
   For each product \( j \):
   \[
   x_j \leq demand_j
   \]

3. **Non-negativity Constraints**:
   For each product \( j \):
   \[
   x_j \geq 0
   \]

\subsection*{Input Format}
The input format for the model is as follows:
\begin{verbatim}
{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}
\end{verbatim}

\subsection*{Output Format}
The output format of the solution will be:
\begin{verbatim}
{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

#### Extract data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

#### Number of products and raw materials
M = len(prices)
N = len(available)

#### Create the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("amount_produced", range(M), lowBound=0)

#### Objective function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

#### Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

#### Demand constraints
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j+1}"

#### Solve the problem
problem.solve()

#### Extract results
amounts = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

#### Output the results
output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

