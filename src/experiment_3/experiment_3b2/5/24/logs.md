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
To model this problem as a Mixed-Integer Linear Program (MIP), we will introduce decision variables for both the operation status of each mine and the amount of ore produced from each mine in each year:

1. Binary decision variable \( \text{isoperated}_{k,i} \) is 1 if mine \( k \) is operated in year \( i \), and 0 otherwise.
2. Continuous decision variable \( \text{amount}_{k,i} \) represents the amount of ore produced by mine \( k \) in year \( i \).

We aim to maximize the net present value (NPV) of profits by selecting which mines to operate each year and how much ore to produce, subject to the given constraints.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets}
\begin{align*}
    & K = \{1, 2, \ldots, n\_mines\} \quad \text{(set of mines)} \\
    & I = \{1, 2, \ldots, n\_years\} \quad \text{(set of years)}
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & \text{royalty}_{k} \quad \text{(yearly royalty for mine } k) \\
    & \text{limit}_{k} \quad \text{(upper limit of ore production for mine } k) \\
    & \text{quality}_{k} \quad \text{(ore quality from mine } k) \\
    & \text{requiredquality}_{i} \quad \text{(required ore quality in year } i) \\
    & \text{price} \quad \text{(price per ton of blended ore)} \\
    & \text{discount} \quad \text{(discount rate)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{isoperated}_{k,i} \in \{0, 1\} \quad \forall k \in K, \forall i \in I \\
    & \text{amount}_{k,i} \geq 0 \quad \forall k \in K, \forall i \in I
\end{align*}

\subsection*{Objective}
Maximize the NPV of profits:
\begin{align*}
    \max \sum_{i \in I} \Bigg(\frac{\text{price}}{(1 + \text{discount})^{i}} \times \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} \text{royalty}_{k} \times \text{isoperated}_{k,i}\Bigg)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \sum_{k \in K} \text{amount}_{k,i} \times \text{quality}_{k} = \text{requiredquality}_{i} \times \sum_{k \in K} \text{amount}_{k,i}, \quad \forall i \in I \\
    & \text{amount}_{k,i} \leq \text{limit}_{k} \times \text{isoperated}_{k,i}, \quad \forall k \in K, \forall i \in I \\
    & \sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \in I
\end{align*}

\end{document}
```

This model aims to maximize the net present value of profits, considering the costs of keeping mines open and the constraints related to ore quality, production limits, and the maximum number of operating mines per year. The first constraint ensures the blended quality requirement is met each year, the second constraint ensures production does not exceed capacity if a mine is operating, and the third limits the number of active mines each year.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets}
\begin{align*}
    & K = \{1, 2, \ldots, n\_mines\} \quad \text{(set of mines)} \\
    & I = \{1, 2, \ldots, n\_years\} \quad \text{(set of years)}
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & \text{royalty}_{k} \quad \text{(yearly royalty for mine } k) \\
    & \text{limit}_{k} \quad \text{(upper limit of ore production for mine } k) \\
    & \text{quality}_{k} \quad \text{(ore quality from mine } k) \\
    & \text{requiredquality}_{i} \quad \text{(required ore quality in year } i) \\
    & \text{price} \quad \text{(price per ton of blended ore)} \\
    & \text{discount} \quad \text{(discount rate)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{isoperated}_{k,i} \in \{0, 1\} \quad \forall k \in K, \forall i \in I \\
    & \text{amount}_{k,i} \geq 0 \quad \forall k \in K, \forall i \in I
\end{align*}

\subsection*{Objective}
Maximize the NPV of profits:
\begin{align*}
    \max \sum_{i \in I} \Bigg(\frac{\text{price}}{(1 + \text{discount})^{i}} \times \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} \text{royalty}_{k} \times \text{isoperated}_{k,i}\Bigg)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \sum_{k \in K} \text{amount}_{k,i} \times \text{quality}_{k} = \text{requiredquality}_{i} \times \sum_{k \in K} \text{amount}_{k,i}, \quad \forall i \in I \\
    & \text{amount}_{k,i} \leq \text{limit}_{k} \times \text{isoperated}_{k,i}, \quad \forall k \in K, \forall i \in I \\
    & \sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \in I
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON format
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

#### Model definition
problem = pulp.LpProblem("Maximize_NPV_of_Profits", pulp.LpMaximize)

#### Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(data['n_mines']) for i in range(len(data['requiredquality']))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(data['n_mines']) for i in range(len(data['requiredquality']))), lowBound=0)

#### Objective function
problem += pulp.lpSum(
    (data['price'] / (1 + data['discount']) ** (i + 1)) * 
    (pulp.lpSum(amount[k, i] for k in range(data['n_mines'])) - 
     pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in range(data['n_mines'])))
    for i in range(len(data['requiredquality'])))
    
#### Constraints
#### Quality constraint
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in range(data['n_mines'])) == data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in range(data['n_mines']))

#### Limit constraint
for k in range(data['n_mines']):
    for i in range(len(data['requiredquality'])):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

#### Max work constraint
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(isoperated[k, i] for k in range(data['n_mines'])) <= data['n_maxwork']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

