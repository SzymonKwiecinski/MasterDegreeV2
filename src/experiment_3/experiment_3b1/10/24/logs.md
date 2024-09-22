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

\section*{Mathematical Model for Mining Operations}

\subsection*{Parameters}

\begin{itemize}
    \item Let \( n_mines \) be the total number of mines.
    \item Let \( n_{maxwork} \) be the maximum number of mines that can operate in any one year.
    \item Let \( royalty_k \) be the yearly royalty payable on mine \( k \).
    \item Let \( limit_k \) be the upper limit of ore that can be extracted from mine \( k \) in a year.
    \item Let \( quality_k \) be the quality of the ore from mine \( k \).
    \item Let \( requiredquality_i \) be the required quality of blended ore in year \( i \).
    \item Let \( price \) be the selling price per ton of blended ore each year.
    \item Let \( discount \) be the discount rate per annum.
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item Let \( isoperated_{k,i} \) be a binary variable that indicates whether mine \( k \) is operated in year \( i \) (1 if operated, 0 otherwise).
    \item Let \( amount_{k,i} \) be the amount of ore produced by mine \( k \) in year \( i \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total profit over the planning horizon:

\[
\text{Maximize } Z = \sum_{i=1}^{I} \left( \frac{price \cdot \sum_{k=1}^{n_{mines}} amount_{k,i}}{(1 + discount)^{i-1}} - \sum_{k=1}^{n_{mines}} royalty_k \cdot isoperated_{k,i} \right)
\]

\subsection*{Constraints}

1. **Operating Mines Limit**:
\[
\sum_{k=1}^{n_{mines}} isoperated_{k,i} \leq n_{maxwork}, \quad \forall i \in \{1, \ldots, I\}
\]

2. **Quality Constraint**:
\[
\sum_{k=1}^{n_{mines}} \frac{quality_k \cdot amount_{k,i}}{\sum_{k=1}^{n_{mines}} amount_{k,i}} = requiredquality_i, \quad \forall i \in \{1, \ldots, I\}
\]

3. **Production Limits**:
\[
amount_{k,i} \leq limit_k \cdot isoperated_{k,i}, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

4. **Open Mines Condition**:
\[
isoperated_{k,i} \in \{0, 1\}, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

5. **Non-negativity**:
\[
amount_{k,i} \geq 0, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

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

\section*{Mathematical Model for Mining Operations}

\subsection*{Parameters}

\begin{itemize}
    \item Let \( n_mines \) be the total number of mines.
    \item Let \( n_{maxwork} \) be the maximum number of mines that can operate in any one year.
    \item Let \( royalty_k \) be the yearly royalty payable on mine \( k \).
    \item Let \( limit_k \) be the upper limit of ore that can be extracted from mine \( k \) in a year.
    \item Let \( quality_k \) be the quality of the ore from mine \( k \).
    \item Let \( requiredquality_i \) be the required quality of blended ore in year \( i \).
    \item Let \( price \) be the selling price per ton of blended ore each year.
    \item Let \( discount \) be the discount rate per annum.
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item Let \( isoperated_{k,i} \) be a binary variable that indicates whether mine \( k \) is operated in year \( i \) (1 if operated, 0 otherwise).
    \item Let \( amount_{k,i} \) be the amount of ore produced by mine \( k \) in year \( i \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total profit over the planning horizon:

\[
\text{Maximize } Z = \sum_{i=1}^{I} \left( \frac{price \cdot \sum_{k=1}^{n_{mines}} amount_{k,i}}{(1 + discount)^{i-1}} - \sum_{k=1}^{n_{mines}} royalty_k \cdot isoperated_{k,i} \right)
\]

\subsection*{Constraints}

1. **Operating Mines Limit**:
\[
\sum_{k=1}^{n_{mines}} isoperated_{k,i} \leq n_{maxwork}, \quad \forall i \in \{1, \ldots, I\}
\]

2. **Quality Constraint**:
\[
\sum_{k=1}^{n_{mines}} \frac{quality_k \cdot amount_{k,i}}{\sum_{k=1}^{n_{mines}} amount_{k,i}} = requiredquality_i, \quad \forall i \in \{1, \ldots, I\}
\]

3. **Production Limits**:
\[
amount_{k,i} \leq limit_k \cdot isoperated_{k,i}, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

4. **Open Mines Condition**:
\[
isoperated_{k,i} \in \{0, 1\}, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

5. **Non-negativity**:
\[
amount_{k,i} \geq 0, \quad \forall k \in \{1, \ldots, n_{mines}\}, \forall i \in \{1, \ldots, I\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

#### Parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)

#### Create the problem
problem = pulp.LpProblem("Mining_Operations_Profit_Maximization", pulp.LpMaximize)

#### Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(I)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[k][i] for k in range(n_mines)) / ((1 + discount)**(i + 1)) - 
    pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) 
    for i in range(I)
)

#### Constraints

#### Operating Mines Limit
for i in range(I):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

#### Quality Constraint
for i in range(I):
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == requiredquality[i] * \
               pulp.lpSum(amount[k][i] for k in range(n_mines))

#### Production Limits
for k in range(n_mines):
    for i in range(I):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

