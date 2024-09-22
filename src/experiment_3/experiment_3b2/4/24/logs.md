# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model: Mixed Integer Programming (MIP)}

\subsection*{Sets and Indices}
\begin{align*}
& K = \{1, 2, \ldots, \text{n\_mines}\} & \text{Set of mines.} \\
& I = \{1, 2, \ldots, \text{number of years}\} & \text{Set of years.}
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{n\_maxwork} & \text{Maximum number of mines that can operate in any one year.} \\
& \text{royalty}_k & \text{Royalty payable for keeping mine $k$ open.} \\
& \text{limit}_k & \text{Maximum ore extraction limit for mine $k$ per year.} \\
& \text{quality}_k & \text{Quality of ore from mine $k$.} \\
& \text{requiredquality}_i & \text{Required quality of blended ore for year $i$.} \\
& \text{price} & \text{Selling price per ton of blended ore.} \\
& \text{discount} & \text{Discount rate per annum.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{isoperated}_{k,i} \in \{0, 1\} & \text{1 if mine $k$ is operated in year $i$, 0 otherwise.} \\
& \text{amount}_{k,i} \geq 0 & \text{Amount of ore produced by mine $k$ in year $i$.}
\end{align*}

\subsection*{Objective Function}
Maximize the discounted profit over the planning horizon:
\begin{align*}
\max \sum_{i \in I} \left(\frac{\text{price} \times \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} (\text{royalty}_k \times \text{isoperated}_{k,i})}{(1 + \text{discount})^i}\right)
\end{align*}

\subsection*{Constraints}
\noindent \textbf{Quality Constraint:}
\begin{align*}
\sum_{k \in K} \text{amount}_{k,i} \times \text{quality}_k = \text{requiredquality}_i \times \sum_{k \in K} \text{amount}_{k,i}, \quad \forall i \in I
\end{align*}

\noindent \textbf{Operational Limit Constraint:}
\begin{align*}
\sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \in I
\end{align*}

\noindent \textbf{Production Limit Constraint:}
\begin{align*}
0 \leq \text{amount}_{k,i} \leq \text{limit}_k \times \text{isoperated}_{k,i}, \quad \forall k \in K, \forall i \in I
\end{align*}

\noindent \textbf{Operation Requirement Constraint:}
\begin{align*}
\text{isoperated}_{k,i} \geq \text{isoperated}_{k,i+1}, \quad \forall k \in K, \forall i \in I - \{n\_years\}
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

\section*{Mathematical Model: Mixed Integer Programming (MIP)}

\subsection*{Sets and Indices}
\begin{align*}
& K = \{1, 2, \ldots, \text{n\_mines}\} & \text{Set of mines.} \\
& I = \{1, 2, \ldots, \text{number of years}\} & \text{Set of years.}
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{n\_maxwork} & \text{Maximum number of mines that can operate in any one year.} \\
& \text{royalty}_k & \text{Royalty payable for keeping mine $k$ open.} \\
& \text{limit}_k & \text{Maximum ore extraction limit for mine $k$ per year.} \\
& \text{quality}_k & \text{Quality of ore from mine $k$.} \\
& \text{requiredquality}_i & \text{Required quality of blended ore for year $i$.} \\
& \text{price} & \text{Selling price per ton of blended ore.} \\
& \text{discount} & \text{Discount rate per annum.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{isoperated}_{k,i} \in \{0, 1\} & \text{1 if mine $k$ is operated in year $i$, 0 otherwise.} \\
& \text{amount}_{k,i} \geq 0 & \text{Amount of ore produced by mine $k$ in year $i$.}
\end{align*}

\subsection*{Objective Function}
Maximize the discounted profit over the planning horizon:
\begin{align*}
\max \sum_{i \in I} \left(\frac{\text{price} \times \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} (\text{royalty}_k \times \text{isoperated}_{k,i})}{(1 + \text{discount})^i}\right)
\end{align*}

\subsection*{Constraints}
\noindent \textbf{Quality Constraint:}
\begin{align*}
\sum_{k \in K} \text{amount}_{k,i} \times \text{quality}_k = \text{requiredquality}_i \times \sum_{k \in K} \text{amount}_{k,i}, \quad \forall i \in I
\end{align*}

\noindent \textbf{Operational Limit Constraint:}
\begin{align*}
\sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \in I
\end{align*}

\noindent \textbf{Production Limit Constraint:}
\begin{align*}
0 \leq \text{amount}_{k,i} \leq \text{limit}_k \times \text{isoperated}_{k,i}, \quad \forall k \in K, \forall i \in I
\end{align*}

\noindent \textbf{Operation Requirement Constraint:}
\begin{align*}
\text{isoperated}_{k,i} \geq \text{isoperated}_{k,i+1}, \quad \forall k \in K, \forall i \in I - \{n\_years\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

#### Constants from the data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

#### Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(
    (price * pulp.lpSum(amount[k, i] for k in range(n_mines)) - 
     pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) /
    ((1 + discount) ** (i + 1))
    for i in range(n_years)
)
problem += profit

#### Constraints

#### Quality Constraint
for i in range(n_years):
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

#### Operational Limit Constraint
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

#### Production Limit Constraint
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

#### Operation Requirement Constraint
for k in range(n_mines):
    for i in range(n_years - 1):
        problem += isoperated[k, i] >= isoperated[k, i + 1]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

