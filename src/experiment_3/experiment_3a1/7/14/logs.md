# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A company produces and sells \var{P} different products. 
- The demand for each product is unlimited, but the company is constrained by cash availability and machine capacity.
- Each unit of the \var{i}-th product requires \var{hour_i} machine hours.
- There are \var{availableHours} machine hours available in the current production period.
- The production costs are \var{cost_i} per unit of the \var{i}-th product.
- The selling prices of the \var{i}-th product is \var{price_i} per unit.
- The available cash is \var{cash}.
- Furthermore, \var{investRate_i} of the sales revenues from the \var{i}-th product will be made available to finance operations during the current period.
- \var{investPercentage_i} is a number between 0 and 1
- The company could increase its available machine hours by \var{upgradeHours}, after spending \var{upgradeCost} for certain repairs. 
- The net income from each product is the revenue we get from selling it minus the production cost and the investment cost.

INPUT FORMAT:

{
    "cash": cash,
    "hour": [hour_i for i in 1, ..., P],
    "cost": [cost_i for i in 1, ..., P],
    "price": [price_i for i in 1, ..., P],
    "investPercentage": [investPercentage_i for i in 1, ..., P],
    "upgradeHours": upgradeHours,   
    "upgradeCost": upgradeCost,
    "availableHours": availableHours,
}

OBJECTIVE: We are aiming at maximizing total net income subject to the cash availability and machine capacity limitations

OUTPUT INFO:

- \var{net_income} shows the net income of the company
- \var{production_i} shows the production quantity of the \var{i}-th product
- \var{upgrade} is a boolean variable that shows whether the company should upgrade its machine capacity or not

OUTPUT FORMAT:

{
    "net_income": net_income,
    "production": [production_i for i in 1, ..., P],
    "upgrade": true/false,
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Production and Sales}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of products
    \item $h_i$: Machine hours required for product $i$, for $i = 1, \ldots, P$
    \item $c_i$: Production cost per unit of product $i$, for $i = 1, \ldots, P$
    \item $p_i$: Selling price per unit of product $i$, for $i = 1, \ldots, P$
    \item $r_i$: Investment rate from sales revenue of product $i$, for $i = 1, \ldots, P$
    \item $x_i$: Production quantity of product $i$, for $i = 1, \ldots, P$
    \item $U$: Upgrade hours available
    \item $U_c$: Cost for upgrading machine hours
    \item $A$: Available machine hours
    \item $C$: Available cash
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i \geq 0$: Quantity of product $i$ to produce
    \item $u \in \{0,1\}$: Upgrade variable (1 if upgrade is chosen, 0 otherwise)
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( p_i x_i - c_i x_i - r_i p_i x_i \right) - U_c \cdot u
\]

\subsection*{Constraints}
1. Machine hours constraint:

\[
\sum_{i=1}^{P} h_i x_i \leq A + U \cdot u
\]

2. Cash availability constraint:

\[
\sum_{i=1}^{P} c_i x_i + U_c \cdot u \leq C
\]

3. Non-negativity constraints:

\[
x_i \geq 0 \quad \forall i \in \{1, \ldots, P\}
\]

4. Upgrade decision variable constraint:

\[
u \in \{0, 1\}
\]

\subsection*{Output Variables}
\begin{itemize}
    \item $\text{net\_income} = Z$
    \item $\text{production} = [x_1, x_2, \ldots, x_P]$
    \item $\text{upgrade} = u$
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

\section*{Linear Programming Model for Production and Sales}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of products
    \item $h_i$: Machine hours required for product $i$, for $i = 1, \ldots, P$
    \item $c_i$: Production cost per unit of product $i$, for $i = 1, \ldots, P$
    \item $p_i$: Selling price per unit of product $i$, for $i = 1, \ldots, P$
    \item $r_i$: Investment rate from sales revenue of product $i$, for $i = 1, \ldots, P$
    \item $x_i$: Production quantity of product $i$, for $i = 1, \ldots, P$
    \item $U$: Upgrade hours available
    \item $U_c$: Cost for upgrading machine hours
    \item $A$: Available machine hours
    \item $C$: Available cash
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i \geq 0$: Quantity of product $i$ to produce
    \item $u \in \{0,1\}$: Upgrade variable (1 if upgrade is chosen, 0 otherwise)
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:

\[
\text{Maximize } Z = \sum_{i=1}^{P} \left( p_i x_i - c_i x_i - r_i p_i x_i \right) - U_c \cdot u
\]

\subsection*{Constraints}
1. Machine hours constraint:

\[
\sum_{i=1}^{P} h_i x_i \leq A + U \cdot u
\]

2. Cash availability constraint:

\[
\sum_{i=1}^{P} c_i x_i + U_c \cdot u \leq C
\]

3. Non-negativity constraints:

\[
x_i \geq 0 \quad \forall i \in \{1, \ldots, P\}
\]

4. Upgrade decision variable constraint:

\[
u \in \{0, 1\}
\]

\subsection*{Output Variables}
\begin{itemize}
    \item $\text{net\_income} = Z$
    \item $\text{production} = [x_1, x_2, \ldots, x_P]$
    \item $\text{upgrade} = u$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

#### Model parameters
P = data['P']
h = data['Hour']
c = data['Cost']
p = data['Price']
r = data['InvestPercentage']
U = data['UpgradeHours']
U_c = data['UpgradeCost']
A = data['AvailableHours']
C = data['Cash']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
u = pulp.LpVariable("Upgrade", cat='Binary')

#### Objective function
problem += pulp.lpSum([p[i] * x[i] - c[i] * x[i] - r[i] * p[i] * x[i] for i in range(P)]) - U_c * u, "Total_Net_Income"

#### Constraints
problem += pulp.lpSum([h[i] * x[i] for i in range(P)]) <= A + U * u, "Machine_Hours_Constraint"
problem += pulp.lpSum([c[i] * x[i] for i in range(P)]) + U_c * u <= C, "Cash_Availability_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

