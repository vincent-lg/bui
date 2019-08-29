# Tutoriel : boutons

Ce tutoriel présentera les boutons de manière détaillée : comment les créer dans [le design de la fenêtre](layout.md), comment faire en sorte que les utilisateurs interagissent avec eux, etc. Commencer avec des boutons est un bon moyen de voir rapidement les avantages, les forces et les faiblesses de BUI.

## Boutons dans le design

Pour créer un bouton dans le design de la fenêtre, utilisez la balise [button](../layout/tag/button.md). Celle-ci doit se trouver à l'intérieur d'une balise [window](../layout/tag/window.md). Voyons la syntaxe de base d'une définition de bouton :

    <button x=0 y=1>Nom du bouton</button>

Comme toujours, vous devez spécifier au moins les attributs `x` et `y`, comme indiqué dans le [tutoriel précédent](layout.md#la-fenêtre-en-grille). Le nom du bouton (ou son "label") est spécifié en tant que [donnée](layout.md#données-de-la-balise) de la balise [button](../layout/tag/button.md).

Voici un exemple plus complet de design créant plusieurs boutons sur la fenêtre :

```
<window title="Présentation des boutons dans BUI">
  <button x=2 y=1>Bouton en haut</button>
  <button x=0 y=3>Bouton à gauche</button>
  <button x=5 y=3>Bouton à droite</button>
  <button x=2 y=5>Bouton en bas</button>
</window>
```

Cela créera une fenêtre avec 4 boutons: un en haut, un à gauche, un à droite et un en bas de la fenêtre.

Les boutons ont davantage d'[attributs](../layout/tag/button.md#attributs), mais le plus important est sans doute `id`. Comme indiqué dans le [tutoriel précédent](layout.md#identifiants-de-widget), les identifiants sont utilisés pour désigner les widgets. Ils constituent le point de contact entre le esign de la fenêtre et les interactions utilisateur. Le concepteur et le développeur doivent connaître ces identifiants.

Un identifiant est une chaîne de caractères identifiant le widget de façon unique. Deux widgets ne peuvent pas avoir le même identifiant. Dans le cas de boutons, BUI essaiera d'inférer un identifiant en utilisant le nom du bouton (son "label") si l'attribut `id` n'est pas spécifié. Bien que cela puisse être extrêmement utile, en particulier dans de petites boîtes de dialogue ou fenêtres, il est toujours recommandé de spécifier un attribut `id` pour chaque bouton :

```
<window title="Présentation des boutons dans BUI">
  <button x=2 y=1 id=haut>Bouton en haut</button>
  <button x=0 y=3 id=gauche>Bouton à gauche</button>
  <button x=5 y=3 id=droite>Bouton à droite</button>
  <button x=2 y=5 id=bas>Bouton en bas</button>
</window>
```

Tout ce que vous avez besoin de dire au développeur en charge des interactions utilisateur, c'est que votre mise en page définit 4 boutons : "haut", "gauche", "droite" et "bas". Le développeur n'a pas besoin de savoir où ils se trouvent et comment ils apparaissent.

Pour connaître et utiliser les autres attributs de `<button>`, voir les [attributs de la balise button](../layout/tag/button.md#attributs).

## Méthodes de contrôle

En tant que développeur, nous serions plus intéressés par la manière d'interagir avec les utilisateurs et de réagir aux actions utilisateurs. Dans ce tutoriel, nous verrons comment gérer les clics sur les boutons.

Vous pouvez commencer par créer un fichier nommé "boutons.py". À l'intérieur de celui-ci, collez le code suivant :

```python
from bui import Window, start

class Boutons(Window):

    """Exemple de boutons dans BUI."""

    # Une fois encore, le design de la fenêtre est inclu directement
    # dans le code ici. Mais il serait préférable de l'écrire
    # dans un fichier séparé (boutons.bui ici)
    layout = mark("""
      <window title="Présentation des boutons dans BUI">
        <button x=2 y=1 id=haut>Bouton en haut</button>
        <button x=0 y=3 id=gauche>Bouton à gauche</button>
        <button x=5 y=3 id=droite>Bouton à droite</button>
        <button x=2 y=5 id=bas>Bouton en bas</button>
        <text x=2 y=3 id=action>Action</text>
      </window>
    """)

    # ... nous écrirons les méthodes de contrôle ici

start(Boutons)
```

C'est presque le même design utilisé dans la section précédente. La seule chose que nous ajoutons est un champ de texte au milieu de la fenêtre pour signaler ce que nous faisons.

### Méthodes de contrôle

Pour intercepter les actions des utilisateurs dans BUI, le processus consiste à créer des méthodes simples dont le nom commence par `on_`. Voyons un premier exemple :

```python
from bui import Window, start

class Boutons(Window):

    """Exemple de boutons dans BUI."""

    # Une fois encore, le design de la fenêtre est inclu directement
    # dans le code ici. Mais il serait préférable de l'écrire
    # dans un fichier séparé (boutons.bui ici)
    layout = mark("""
      <window title="Présentation des boutons dans BUI">
        <button x=2 y=1 id=haut>Bouton en haut</button>
        <button x=0 y=3 id=gauche>Bouton à gauche</button>
        <button x=5 y=3 id=droite>Bouton à droite</button>
        <button x=2 y=5 id=bas>Bouton en bas</button>
        <text x=2 y=3 id=action>Action</text>
      </window>
    """)

    def on_haut(self):
        """Le bouton en haut a été cliqué."""
        self["action"].value = "Le bouton en haut a été cliqué."

start(Boutons)
```

Si vous exécutez ce code, la fenêtre devrait apparaître. Si vous cliquez (ou appuyez sur la touche RETOUR) sur le bouton du haut, le champ de texte sera mis à jour : il devrait contenir "Le bouton du haut a été cliqué".

Nous avons ajouté seulement 3 lignes (2 sans compter la docstring). Voyons ce qu'elles font :

- Nous commençons par créer une nouvelle méthode sur la fenêtre, appelée `on_haut`. `on_` est le préfixe d'une méthode de contrôle, indiquant à BUI que cette méthode doit être liée à un contrôle. `haut` est la seule information restante. BUI comprend que nous souhaitons associer cette méthode de contrôle à l'action "l'utilisateur clique sur le bouton de l'ID haut" ;
- Dans cette méthode, nous appelons `self["action"]`. Ce code renvoie le widget d'ID "action". Si vous regardez notre design, vous verrez qu'il s'agit du widget de type texte. Nous mettons à jour sa valeur (le texte qu'il contient) en utilisant une propriété simple (`self["action"].value = "texte à afficher"`).

Nous pourrions relier n'importe quel autre bouton de la même manière. Par exemple :

```python
from bui import Window, start

class Boutons(Window):

    """Exemple de boutons dans BUI."""

    # Une fois encore, le design de la fenêtre est inclu directement
    # dans le code ici. Mais il serait préférable de l'écrire
    # dans un fichier séparé (boutons.bui ici)
    layout = mark("""
      <window title="Présentation des boutons dans BUI">
        <button x=2 y=1 id=haut>Bouton en haut</button>
        <button x=0 y=3 id=gauche>Bouton à gauche</button>
        <button x=5 y=3 id=droite>Bouton à droite</button>
        <button x=2 y=5 id=bas>Bouton en bas</button>
        <text x=2 y=3 id=action>Action</text>
      </window>
    """)

    def on_haut(self):
        """Le bouton en haut a été cliqué."""
        self["action"].value = "Le bouton en haut a été cliqué."

    def on_gauche(self):
        """Le bouton à gauche a été cliqué."""
        self["action"].value = "Le bouton à gauche a été cliqué."

start(Boutons)
```

### Plus loin dans les méthodes de contrôle

Examinons plus en détail comment BUI lie les méthodes de contrôle aux actions de l'utilisateur. Nous avons vu que créer une méthode appelée `on_haut` suffisait à faire savoir à BUI que nous voulions intercepter l'action "un utilisateur clique sur le bouton de l'ID haut". Mais cela semble impliquer que nous ne pouvons réagir qu'au clic, du moins sur les boutons. Heureusement, ce n'est pas le cas.

BUI utilise l'introspection pour lier les actions des utilisateurs aux méthodes de contrôle. Il examine le nom de la méthode de contrôle et essaie d'en déduire des informations, dans des limites raisonnables. Le nom complet de la méthode ressemble à cela :

- `on_` : le préfixe d'une méthode de contrôle ;
- `{contrôle}` : le type de contrôle ;
- `_` : un autre trait de soulignement ;
- `{widget}` : l'identifiant du widget.

Que sont les contrôles ? Vous pouvez les imaginer comme des actions de l'utilisateur. Lorsque l'utilisateur clique sur le bouton du haut, BUI génère un contrôle "clic" et le déclenche sur le widget d'ID "haut". Ainsi, la solution pour intercepter le contrôle "clic" sur le widget d'ID "haut" serait de créer une méthode nommée `on_click_haut`. Vous pouvez essayer avec le même design de la fenêtre pour lier une méthode au bouton droit:

```python
    def on_click_droit(self):
        """Le bouton à droite a été cliqué."""
        self["action"].value = "Le bouton à droite a été cliqué."
```

Donc... `on_click_droit` ou `on_droit` font la même chose ? Étrange.

BUI utilise un système de contrôles implicites sur différents widgets. Quand une méthode `on_haut` est définie, BUI réalise que "haut" est un bouton. Quel serait l'action la plus probable ? BUI répond : "Je suppose que nous voulons intercepter le moment où l'utilisateur clique sur le bouton". Donc `on_haut` et `on_click_haut` font la même chose.

> L'utilisation de contrôles implicites peut sembler dangereuse. Mieux vaut spécifier le nom du contrôle explicitement à chaque fois. Cependant, sur certains widgets, l'écriture explicite du nom du contrôle ne facilite pas la lecture. Vous devrez décider de la stratégie à utiliser dans l'un ou l'autre cas.

### Méthodes de contrôle asynchrones

Dans l'exemple précédent, la méthode de contrôle réagit directement au contrôle. L'action n'est pas terminée jusqu'à la fin de l'exécution de la méthode de contrôle. Mais BUI implémente une fonctionnalité intéressante pour permettre à une méthode de contrôle de s'exécuter plus longtemps sans bloquer la fenêtre.

Ajoutons une nouvelle méthode pour voir comment cela fonctionne :

```python
    async def on_bas(self, widget):
        """Le bouton du bas a été cliqué."""
        action = self["action"]
        action.value = (
                "Super ! Jouons à cache-cache ! Tu te caches et je compte."
        )

        # Compter de 1 à 20 en 20 secondes
        for i in range(1, 21):
            widget.name = f"{i}"
            await self.sleep(1)

        action.value = "Tu es caché ? J'arrive !"
```

Exécutez la fenêtre et cliquez sur le bouton du bas. Vous verrez du texte s'afficher au milieu de la fenêtre, puis le bouton change son nom (son "label") de "Bouton du bas" à "1". Après une seconde, le bouton devient "2". Etc. Cela ne bloque pas la fenêtre. Vous pouvez cliquer sur d'autres boutons. D'ailleurs, vous pouvez cliquer sur le bouton du bas une fois de plus, ce qui créera deux boucles parallèles et pourrait donner des résultats bizarres (nous verrons comment gérer cela dans la section suivante).

Pour le moment, regardons le code :

- D'abord, vous avez le mot clé `async` devant la définition de la méthode. Il s'agit d'un mot-clé standard de Python pour indiquer que la fonction (méthode dans notre cas) est asynchrone (son traitement peut prendre un certain temps et son contenu ne doit pas bloquer le reste de l'application).
- Le nom de la méthode est similaire. Il obéit aux mêmes règles (nous utilisons `on_bas` ici, comme indiqué ci-dessus, nous aurions pu écrire `on_click_bas` avec le même résultat).
- Nous avons un argument supplémentaire dans la méthode, `widget`. Il n'est pas spécifique aux méthodes asynchrones. C'est juste un raccourci (cet argument contiendra le widget du bouton sur lequel nous avons cliqué). Les méthodes de contrôle acceptent une large gamme d'arguments.
- Nous capturons d'abord le texte d'identifiant "action" dans une variable. Ce widget sera utilisé plusieurs fois dans notre méthode, pas besoin de le rechercher à chaque fois que nous voulons le modifier.
- Nous mettons à jour le contenu du widget "action".
- Ensuite se trouve une boucle qui doit tourner 20 fois. À l'intérieur, il n'y a que deux actions :

   - Tout d'abord, nous modifions le nom du widget (le bouton "bas") avec une propriété. Ceci mettra à jour le nom du bouton (son "label") à l'écran.
   - Nous utilisons ensuite le mot-clé `await` et faisons une pause d'une seconde. Pour ce faire, nous appelons la méthode [sleep](../widget/Window.md#sleep) de la fenêtre qui crée une pause asynchrone. Pendant ce temps, la fenêtre reprend son activité normale (vous pouvez cliquer sur d'autres choses, par exemple). Après cette seconde, la boucle recommence...

- ... jusqu'à atteindre `i > 20`. À ce stade, nous sortons de la boucle, mettons à jour le texte une dernière fois et la méthode se termine.

Bien que légère, cette fonctionnalité peut ne pas sembler strictement nécessaire à première vue. Mais considérez, par exemple, que vous pouvez télécharger un fichier (comme la mise à jour du logiciel) sans bloquer le reste de l'application, sans exécuter la mise à jour dans un thread ou un processus séparé (ce qui facilite grandement la mise à jour).

### Le contrôle init

Dans l'exemple précédent, nous avons une méthode de contrôle asynchrone, connectée à un bouton sur lequel nous pouvons cliquer plusieurs fois. Cela mène à beaucoup de mises à jour et à des changements confus dans le nom du bouton (son "label"). Par exemple, le bouton arrive sur "3", "4", puis reviens à "1", puis "6", puis "2"... Dans ce cas, nous aurions besoin de dire à Python de ne pas exécuter le compteur de "cache-cache" s'il est déjà en cours d'exécution... et d'attendre qu'il soit fini avant de l'autoriser à nouveau.

Il y a différentes options. Mais un bon moyen serait de stocker l'état dans une variable et d'éviter d'exécuter le compteur de "cache-cache" si cet état indique qu'il est déjà en train de compter. Il serait plus facile de stocker cette information dans l'objet `window` lui-même, afin que nous puissions y accéder grâce à `self` dans notre méthode de contrôle. Mais nous devons créer cette variable (cet attribut d'instance) avant l'exécution du contrôle.

Le contrôle `init` peut être utilisé à cette fin. Il est appelé pour chaque widget (y compris la fenêtre) lorsqu'il est prêt à être affiché, mais avant qu'il ne soit réellement affiché. Vous pouvez imaginer `init` comme une méthode équivalente à la méthode spéciale `__init__`, bien que vous ne deviez pas remplacer la méthode spéciale `__init__` dans votre fenêtre.

`init` est un contrôle. Il suffit donc de créer une méthode pour l'intercepter. Sauriez-vous le faire ?

```python
    def on_init_bas(self):
        """Le bouton en bas est prêt à être affiché, mais n'est pas encore affiché."""
        self.cache_cache = False
```

Voyons donc un exemple complet d'utilisation de cette fonctionnalité :

```python
class Boutons(Window):

    """Exemple de boutons dans BUI."""

    # ... design de la fenêtre et autres méthodes de contrôle

    def on_init_bas(self):
        """Le bouton en bas est prêt à être affiché, mais n'est pas encore affiché."""
        self.cache_cache = False

    async def on_bas(self, widget):
        """Le bouton du bas a été cliqué."""
        action = self["action"]
        if self.cache_cache:
            action.value = "Je compte déjà ! Dépêche-toi et va te cacher !"
            return

        self.cache_cache = True
        action.value = (
                "Super ! Jouons à cache-cache ! Tu te caches et je compte."
        )

        # Compter de 1 à 20 en 20 secondes
        for i in range(1, 21):
            widget.name = f"{i}"
            await self.sleep(1)

        action.value = "Tu es caché ? J'arrive !"
        self.cache_cache = False
```

Le code ajouté est vraiment court. Si vous exécutez ce code et cliquez sur le bouton du bas, le compteur de "cache-cache" commence. Mais si vous cliquez à nouveau sur le même bouton pendant que le compteur est en cours d'exécution, le texte du milieu indiquera que le compteur est déjà en cours d'exécution et ne l'exécutera pas. Tout cela grâce à un attribut d'instance pour conserver l'état !

## Conclusion

C'était une première démonstration des capacités et de la simplicité de BUI, mais aussi de sa flexibilité. La flexibilité a un prix. Bien que ce document traite de certains pièges à éviter, vous pourriez avoir du mal à naviguer dans la logique du design de la fenêtre et de méthodes de contrôle par vous-même, pour l'heure. Mais heureusement, il existe davantage de tutoriels et encore plus de documentation pour vous aider.

- [Lire la documentation complète de la balise button](../layout/tag/button.md)
- [En savoir plus sur les contrôles](../control/overview.md)
- [Une fenêtre avec une barre de menu](menubar.md)
- [Gestion des raccourcis clavier](keyboard.md)
- [Cases à cocher et boutons radio](choices.md)
- [Listes et tableaux](lists.md)
- [Boîtes de dialogue](dialogs.md)
