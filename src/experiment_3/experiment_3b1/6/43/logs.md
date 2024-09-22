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

\section*{Linear Programming Model for Production Optimization}

\textbf{Parameters:}
\begin{itemize}
    \item $M$: Number of different products
    \item $N$: Number of different raw materials
    \item $available_i$: Available units of raw material $i$, for $i = 1, \ldots, N$
    \item $req_{i,j}$: Units of raw material $i$ required for product $j$, for $j = 1, \ldots, M$ and $i = 1, \ldots, N$
    \item $price_j$: Selling price per unit of product $j$, for $j = 1, \ldots, M$
    \item $cost_j$: Production cost per unit of product $j$, for $j = 1, \ldots, M$
    \item $demand_j$: Maximum forecasted demand for product $j$, for $j = 1, \ldots, M$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_j$: Amount of product $j$ to be produced, for $j = 1, \ldots, M$
\end{itemize}

\textbf{Objective Function:}

Maximize total profit:
\[
\text{Total Profit} = \sum_{j=1}^{M} (price_j - cost_j) \cdot amount_j
\]

\textbf{Subject to:}
\begin{itemize}
    \item Raw Material Constraints:
    \[
    \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \text{for } i = 1, \ldots, N
    \]
    
    \item Demand Constraints:
    \[
    amount_j \leq demand_j \quad \text{for } j = 1, \ldots, M
    \]
    
    \item Non-negativity:
    \[
    amount_j \geq 0 \quad \text{for } j = 1, \ldots, M
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

\section*{Linear Programming Model for Production Optimization}

\textbf{Parameters:}
\begin{itemize}
    \item $M$: Number of different products
    \item $N$: Number of different raw materials
    \item $available_i$: Available units of raw material $i$, for $i = 1, \ldots, N$
    \item $req_{i,j}$: Units of raw material $i$ required for product $j$, for $j = 1, \ldots, M$ and $i = 1, \ldots, N$
    \item $price_j$: Selling price per unit of product $j$, for $j = 1, \ldots, M$
    \item $cost_j$: Production cost per unit of product $j$, for $j = 1, \ldots, M$
    \item $demand_j$: Maximum forecasted demand for product $j$, for $j = 1, \ldots, M$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_j$: Amount of product $j$ to be produced, for $j = 1, \ldots, M$
\end{itemize}

\textbf{Objective Function:}

Maximize total profit:
\[
\text{Total Profit} = \sum_{j=1}^{M} (price_j - cost_j) \cdot amount_j
\]

\textbf{Subject to:}
\begin{itemize}
    \item Raw Material Constraints:
    \[
    \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \text{for } i = 1, \ldots, N
    \]
    
    \item Demand Constraints:
    \[
    amount_j \leq demand_j \quad \text{for } j = 1, \ldots, M
    \]
    
    \item Non-negativity:
    \[
    amount_j \geq 0 \quad \text{for } j = 1, \ldots, M
    \end{itemize}
\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Parameters
M = len(data['prices'])  #### Number of products
N = len(data['available'])  #### Number of raw materials
available = data['available']
req = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

#### Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective Function: Maximize total profit
problem += pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M)), "Total_Profit"

#### Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(req[i][j] * amount[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i}"

#### Constraints for demand
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

