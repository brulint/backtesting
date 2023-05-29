# Backtest

Keep it simple and stupid backstesting trading strategies.

## Disclamer

_Quod de futuris non est determinata omnino veritas._

## Download data

Soit le cour d'un actif (ici BTC au 29/05/2023 - périodes de 2h):

```python
              time     open     high      low    close      volume         count
0     1.664438e+09  20119.9  20119.9  19968.2  20053.4  138.364192  2.771255e+06
1     1.664446e+09  20053.5  20127.8  20002.1  20097.5   86.577967  1.737841e+06
2     1.664453e+09  20103.6  20111.4  19956.9  20010.3  169.203402  3.390640e+06
3     1.664460e+09  20022.2  20028.8  19453.0  19503.0  317.729294  6.274010e+06
4     1.664467e+09  19501.3  19802.1  19386.0  19746.2  230.254841  4.505230e+06
...            ...      ...      ...      ...      ...         ...           ...
2896  1.685290e+09  25296.0  25296.0  25295.9  25296.0    0.012348  3.123668e+02
2897  1.685297e+09  25381.0  25500.0  25344.7  25454.5   49.642965  1.261837e+06
2898  1.685304e+09  25457.0  25457.0  25429.8  25429.8    1.014275  2.579427e+04
2899  1.685311e+09  25629.5  26000.0  25629.5  25942.3   95.758923  2.472821e+06
2900  1.685318e+09  25942.3  25994.5  25942.3  25982.3    0.775963  2.015425e+04

[2901 rows x 7 columns]
```

<p align="center"><img src="img/20230520_001.png" /></p>

## Strategy

Intuitivement, un cours qui commence à remonter est un signal d'achat et un cours qui commence à redescendre est un signal de vente. Pour ça, le RSI est notre ami.

<p align="center"><img src="img/20230520_002.png" /></p>

Signaux:

$$
\begin{align} SIG_{buy} &= \big\[ \  RSI_{14}(t_{n-1}) < 30 \  \big\]  \  \\& \  \big\[ \  RSI_{14}(t_n) > 30 \  \big\]
        \\\\ SIG_{sell} &= \big\[ \  RSI_{14}(t_{n-1}) > 70 \  \big\] \  \\& \  \big\[ \  RSI_{14}(t_n) < 70 \  \big\]
        \\\\ SIG(t_n)   &= \begin{cases} 1 & \Leftarrow  SIG_{buy} = 1
                                   \\\\ -1 & \Leftarrow  SIG_{sell} = 1
                           \end{cases}
\end{align}
$$

<p align="center"><img src="img/20230520_003.png" /></p>

Position: 

$$POS(t_n) = \begin{cases} SIG(t_n) & \Leftarrow SIG(t_n) \neq 0 \\\\ POS(t_{n-1}) & \end{cases}$$

<p align="center"><img src="img/20230520_004.png" /></p>


En python:

```python
SIG_buy = (RSI.shift() < 30) & (RSI > 30)
SIG_sell = (RSI.shift() > 70) & (RSI < 70)
SIG = SIG_buy.astype(int) - SIG_sell.astype(int)
POS = SIG_0.where(SIG_0 != 0).ffill()
POS_buy = df.close.where((POS == 1) & (POS.shift() == -1))
POS_sell = df.close.where((POS == -1) & (POS.shift() == 1))
```

<p align="center"><img src="img/20230520_005.png" /></p>

## Rendement

Rendement en HODL:

$$r_0(t_n) = r_0([t_{n-1},t_n]) = { Price(t_n)\over Price(t_{n-1}) }$$

Interprétation du signal $POS$:

$$\begin{array}{cc|c} POS(t_{n-1}) & POS(t_n) & r_{strat}([t_{n-1},t_n]) \\\\ \hline -1 & -1 & 1 \\\\ -1 & 1 & 1 \\\\ 1 & 1 & r_0([t_{n-1},t_n]) \\\\ 1 & -1 & r_0([t_{n-1},t_n]) \\\\ \end{array}$$

Rendement de la stratégie:

$$r_{strat}(t_n) = r_{strat}([t_{n-1},t_n]) = \begin{cases} r_0(t_n) & \text{if } POS(t_{n-1}) = 1 \\\\ 1 & \text{else} \end{cases}$$

<p align="center"><img src="img/20230520_006.png" /></p>

Sans oublier les fees: Lors de chaque transaction (achat et vente), la plateforme prend un fee équivalent à $fee%$:

Même raisonnement que plus haut:

$$r_{fee}(t_n) = \begin{cases} 1-fee & \text{if } POS(t_{n-1}) + POS(t_n) = 1 \\\\ 1 & \text{else} \end{cases}$$

Rendement cumulé:

$$R(t_n) = \prod_{i=1}^{t_n} \biggl( r_{strat}(i) \times r_{fee}(i) \biggr)$$

<p align="center"><img src="img/20230520_007.png" /></p>

Avec:

  - en grisé, le rendement cumulé en HODL
  - en bleu, le rendement brut cumulé de la stratégie
  - en rouge, le rendement net cumulé de la stratégie

