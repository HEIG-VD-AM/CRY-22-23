# CRY-22-23

| Lab | Note |
|-----|------|
| 1   | 6    |
| 2   | 6    |
| 3   | 6    |
| 4   | 5.7  |

On retrouve aussi un notebook Jupyter/Sage qui est plutôt lié au cours.
Celui-ci contient les formules qui permettent de faire tous les calculs requis pour le cours de CRY.
Je suis désolé pour la qualité du notebook que je ne comptais pas poster publiquement à la base, il faudra donc comprendre le but de chaque cellule.
J'ai fait en sorte de faire certaines formules à la main au lieu d'utiliser les méthodes Sage afin d'avoir accès au développement à chaque étape.
Il s'avère donc très pratique pour se corriger en exercice ou pour vérifier ses réponses lors de l'examen intermédiaire par exemple (si c'est encore autorisé).

Pour l'utiliser c'est assez facile, si vous avez installé Sage en natif sur votre machine, vous pouvez taper la commande suivante dans votre terminal :

```
sage -n jupyter
```

Si comme moi vous préférez passer des containers Docker pour ne pas polluer votre machine :

```
docker run -p 8888:8888 sagemath/sagemath-jupyter
```

A noter que cette manière n'est pas persistante et qu'il faudrait faire un simple fichier `docker-compose` avec un volume pour que ça soit le cas.
