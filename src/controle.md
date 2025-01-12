# Controle de flot

Un programme peut ne pas se contenter d'une éxécution squentielle (une suite d'opérations).

Python a la particularité d'utiliser des indentations pour définir les blocs.
Par convention, l'indentation est de quatre espaces. Dans les éditeurs de texte qui reconnaissent Python, une tabulation (la touche "->|" tout à gauche) va créer quatre espaces.

## if/else : Si, sinon

```python
a = True
if a:
    print("yeaaah")
```

```python
a = "ok"
if a == "ok":
    print("Oui")
else:
    print("Non")
```

## for : Pour

Une boucle for va utiliser un *itérateur*, qui pourra être une *collection*, ou plus simplement la fonction `range`.

```
>>> for i in range(3):
...     print(i)
...
0
1
2
```

`range(n)` va compter de `0` jusqu'à `n-1`.

```
>>> for lettre in "abc":
...     print(lettre)
...
a
b
c
```

## while : Tant que

Parfois, on ne sait combien de fois on va boucler.
On va donc itérer jusqu'à ce qu'une clause soit vrai.

```
>>> a = 0
>>> while a < 2:
...     a = a + 1
...
>>> print(a)
2
```

## ハッキング Hakkingu

Avec `if` et `else` il existe `elif` contraction de `else if`.

Avec `break`, il est possible d'interrompre une boucle `for`

```
>>> for i in range(3000):
...     print(i)
...     if i == 2:
...             break
...
0
1
2
```

Il est possible de passer à l'itération suivante d'une boucle `for` avec `continue`.
