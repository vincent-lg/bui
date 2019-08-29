# Design de la fenêtre dans BUI

Comme expliqué dans le [tutoriel précédent](structure.md), le design dans BUI est censé être indépendant du code. Il est ainsi espéré que la conception graphique sera assurée par les concepteurs n'ayant pas nécessairement des compétences de programmation, tandis que les actions de l’utilisateur sont interceptées par les développeurs au moyen du code. Ce tutoriel développe le design de la fenêtre dans BUI : comment l'écrire, sa syntaxe de balises et d'attributs et sa représentation de base dans la fenêtre.

## Où l'écrire ?

Le design BUI peut être défini [dans le code de la fenêtre](../layout/code.md). La plupart des exemples de cette documentation le feront d'ailleurs, afin de rester autonomes. Mais le design peut (et devrait) être écrit dans un fichier séparé : un fichier `.bui` portant le même nom que le fichier Python contenant la classe `Window`.

Ainsi, utilisant [l'exemple basique](../example/basic.md), voyons comment cela pourrait fonctionner :

1. Créez un fichier, nommé `basique.bui`. Ouvrez-le avec un éditeur standard (comme notepad++ ou Vim) et écrivez le design dedans :

   ```
   <window title="Une démonstration avec BUI">
     <menubar>
       <menu name=Fichier>
         <item>Qu'est-ce que c'est ?</item>
         <item>Quitter</item>
       </menu>
     </menubar>

     <button x=2 y=2>Cliquer ici !</button>
     <text x=3 y=3 id=action>Action</text>
   </window>
   ```

2. Créez un fichier dans le même dossier, nommé `basique.py`. Dans celui-ci, écrire le code Python :

   ```python
   from bui import Window, start

   class HelloBUI(Window):

       """Classe représentant un exemple basique avec BUI."""

       def on_cliquer_ici(self):
           """Quand le bouton "Cliquer ici !" est cliqué."""
           self["action"].value = "Le bouton a été cliqué !"

       def on_quitter(self):
           """Quand l'utilisateur sélectionner Quitter dans le menu Fichier."""
           self.close()

       # Raccourcis claviers
       def on_press_alt_f4(self):
           """L'utilisateur appuie sur Alt + F4."""
           self.close()

       # Placer un alias sur une méthode est tellement simple
       on_press_ctrl_q = on_press_alt_f4


   start(HelloBUI)
   ```

3. Exécutez ce script avec Python :

       python basique.py

Il devrait afficher la [fenêtre de l'exemple basique](../example/basic.md). L'avantage ici est que nous avons séparé le design de la fenêtre et le code source : le design est dans un fichier, les concepteurs graphiques peuvent l'éditer sans se soucier du code, alors que le code ne contient que Python, pas le design BUI.

## Syntaxe du design de fenêtre BUI

Le design dans BUI n'est pas définie comme code Python. Il utilise une sorte de syntaxe HTML qui peut sembler familière à certains, mais étrange à d'autres. Cette section décrit plus en détail la syntaxe du design dans BUI. Si ce que vous avez écrit dans `basique.bui` semble évident, vous pouvez passer cette section.

### Balises

Les balises sont les éléments de base du design dans BUI. Elles se trouvent entre un signe inférieur (`<`) et un signe supérieur (`>`). En vérité, leur nom commence juste après un signe inférieur (`<`).

Par exemple, considérons la première ligne du design :

    <window title="Une démonstration avec BUI">

Dans ce contexte, la balise est `window`. C'est le premier mot après l'ouverture de la balise (après le signé inférieur).

Ou bien, à  la ligne suivante :

    <menubar>

`menubar` est la balise. Cette fois, le signe de fin de balise (`>`) suit le nom de la balise. Nous verrons pourquoi lorsque nous parlerons des attributs.

#### Balises d'ouverture et de fermeture

Cette syntaxe définit une balise d'ouverture. Un signe inférieur (`<`), le nom de la balise, éventuellement un espace et des informations supplémentaires, puis un signe supérieur (`>`). Mais il existe une autre syntaxe pour fermer la balise : un signe inférieur (`<`), une barre oblique (`/`), le nom de la balise et le signe supérieur (`>`).

Ainsi, la balise `menubar` est ouverte à la ligne 2 :

    <menubar>

Et elle est refermée à la ligne 7 :

    </menubar>

Entre la balise d'ouverture et celle de fermeture peuvent se trouver des balises imbriquées. Cela permet de créer une hiérarchie simple ou complexe de balises. Élaborons sur ce sujet.

La balise `menubar` s'ouvre à l'intérieur de la balise `window`. Regardez ces lignes :

    <window title="Une démonstration avec BUI">
      <menubar>

La balise `window` n'est pas refermée, la balise `menubar` s'ouvre à l'intérieur. En fait, si vous regardez ce design, vous remarquerez que la balise `window` n’est pas refermée avant la toute dernière ligne. Donc tout le reste est contenu dans la balise `window`. Voyons ce qui est contenu dans la balise `menubar` :

      <menubar>
        <menu name=Fichier>
          <item>Qu'est-ce que c'est ?</item>
          <item>Quitter</item>
        </menu>
      </menubar>

La balise `menu` est définie à l'intérieur de la balise `menubar`. Qu'en est-il des balises `item`? Elles sont définies à l'intérieur de la balise `menu`. Il y a deux éléments dans le menu :

          <item>Qu'est-ce que c'est ?</item>
          <item>Quitter</item>

Pour ces balises, vous remarquerez que nous les fermons immédiatement, elles ne contiennent pas d'autres balises.

Cette hiérarchie est importante. Toutes les balises ne peuvent pas être définies n'impore où. BUI vous avertira si le design n'est pas correcte. Contrairement au HTML, la syntaxe doit être correcte et cohérente : n'ouvrez pas une balise que vous ne fermez pas, fermez les balises dans le même ordre que vous les avez ouvert, les balises imbriquées doivent être spécifiées dans les balises-parentes correctes.

Ainsi, les premières lignes définissent une barre de menus. Et les dernières ? Essayez de deviner quelle balise est le parent de `<button>`.

Si vous avez deviné `<window>`, vous avez raison. La balise `<button>` est définie après la fermeture de la balise `menubar`.

> L'indentation permet de mieux comprendre la hiérarchie des balises d'ouverture et de fermeture. Contrairement à Python, cette indentation n’est pas obligatoire, mais elle vous aidera à distinguer la structure de la fenêtre et vous évitera d’ouvrir des balises et d’oublier de les refermer le moment venu.

### Attributs de balises

Les balises peuvent avoir différents attributs. Les attributs sont définis après le nom de la balise, entre le signe inférieur et le signe supérieur. Un espace les sépare du nom de la balise, ainsi que les uns des autres (une balise peut avoir plusieurs attributs). Les attributs sont utilisés pour donner plus d'informations sur la balise. Par exemple :

        <menu name=Fichier>

On dit que la balise `<menu>` a une attribut `name` ayant pour valeur `Fichier`.

Voyons un autre exemple:

      <text x=3 y=3 id=action>Action</text>

La balise `text` a trois attributs : `x`, `y` et `id`, chacun avec sa propre valeur. Un autre exemple ?

    <window title="Une démonstration avec BUI">

La balise `window` n’a qu’un seul attribut : `title` (le titre de la fenêtre). Notez que nous entourons le titre de guillemets doubles (`"`). Cela est dû au fait que le titre de la fenêtre contient plusieurs mots (il coomprend des espaces). Si nous omettons les guillemets doubles, BUI ne pourra pas savoir où le nom de l'attribut commence et où la valeur de l'attribut se termine.

> En HTML, vous trouverez presque toujours des guillemets doubles autour des valeurs d'attribut, même si la valeur de l'attribut est contenue dans un seul mot. Ce n'est pas obligatoire, mais vous pouvez suivre cette convention si vous ne savez pas quand utiliser des guillemets doubles ou non. Cela ne change rien pour BUI :

        <menu name=Fichier>

Est strictement équivalent à :

        <menu name="Fichier">

Ainsi, si vous voulez ajouter des guillemets doubles autour de toutes les valeurs d'attribut, vous pouvez le faire.

#### Attributs obligatoires ou facultatifs

Certains attributs sont obligatoires, d'autres facultatifs. BUI vous aidera à déterminer lequel est lequel. Tout d’abord, lorsque vous utilisez une balise, vérifiez sa documentation : BUI fournit une documentation détaillée de chaque balise. Par exemple, vous voulez utiliser la balise `button`. Rendez-vous simplement dans la [documentation de la balise button](../layout/tag/button.md). Dedans se trouve une section sur les attributs de la balise avec un tableau listant ceux-ci. Pour chaque attribut, le fait qu'il soit obligatoire ou facultatif est clairement indiqué.

Par exemple, si vous consultez les [attributs de la balise button](../layout/tag/button.md#attributs), vous verrez que seuls `x` et `y` sont obligatoires. Vous ne pouvez donc pas définir un bouton sans le placer sur la fenêtre (ce qui est assez logique). Si vous essayez de supprimer l’un de ces attributs, BUI vous en avertira et n’affiche pas la fenêtre du tout.

D'un autre côté, si vous consultez les [attributs de la balise text](../layout/tag/text.md#attributs), vous verrez que l'attribut `id` n'est pas obligatoire. Cela ne signifie pas que nous ne pouvons pas l'utiliser dans notre balise, ce n'est simplement pas toujours nécessaire :

      <text x=3 y=3 id=action>Action</text>

#### Attributs sans valeur

Certains attributs ne nécessitent pas de valeur. Leur présence suffit pour savoir quoi faire. Spécifiez le nom de l'attribut, mais aucun signe égal (`=`) ou valeur n'est nécessaire. Là encore, en consultant les [attributs de la balise text](../layout/tag/text.md#attributs), vous devriez voir l’attribut `multiline` :

> `multiline`: si présent, place le texte sur plusieurs lignes.

Cet attribut ne nécessite pas de valeur. S'il est présent, le texte peut contenir plusieurs lignes. Si ce n'est pas le cas, le texte reste écrit sur une seule ligne. Pour définir le widget `text` d'ID `action` dans notre design comme texte multiligne, on doit donc écrire quelque chose comme :

      <text x=3 y=3 id=action multiline>Action</text>

Les attributs sans valeur sont généralement indiqués après les autres dans le corps de la balise. Ce n'est absolument pas nécessaire, mais cela pourrait aider les autres à lire votre design.

Pour chaque attribut, vous verrez un bref exemple d'utilisation. Il vous est encouragé de lire cet exemple car il pourrait vous donner plus d'informations sur l'utilisation de l'attribut dans son contexte.

### Données de la balise

Enfin, un dernier élément concernant les balises : leurs données. Les données de balise sont écrites en dehors des signes inférieur et supérieur, entre les balises d'ouverture et de fermeture :

          <item>Qu'est-ce que c'est ?</item>

Ici, "Qu'est-ce que c'est ?" forme les données de la balise `item`.

Les données de balise sont en quelque sorte un type d'attribut (elles sont en fait documentées en tant que telles) : elles possèdent différentes significations pour différentes balises, certaines balises ne nécessitent aucune donnée. À l'intérieur de [la balise item](../layout/tag/item.md), les données doivent contenir le nom de l'élément de menu. Elles sont obligatoires. Si absentes, BUI générera une erreur.

Les données de balises ne nécessitent pas de guillemets, même si elles sont contenues dans plusieurs mots. Le signe inférieur (`<`) suivant devrait simplement indiquer la fin des données.

En règle générale, les balises contenant des balises imbriquées ne contiennent souvent pas de données qui leur sont propres. Bien que la syntaxe reste compréhensible, elle n’est peut-être pas si claire, de sorte que les balises avec des données ne contiennent généralement pas de balises imbriquées en même temps.

## La fenêtre en grille

BUI définit la fenêtre comme une simple grille sur laquelle vous pouvez placer des widgets. Ce concept est extrêmement important pour le design. Vous avez peut-être remarqué que chaque widget doit être placé sur la fenêtre avec les attributs `x` et `y`. Voyons donc ce que ces attributs signifient :

Par défaut, lorsque BUI crée une fenêtre, il génère une grille invisible de 6 sur 6. `x` est le nombre de colonnes sur cette grille (à partir de 0) et `y` est le nombre de lignes sur cette grille (à partir de 0 également). Le widget situé à `x=0` `y=0` est placé dans le coin supérieur gauche de la fenêtre. Avec une grille de 6 par 6 (les valeurs par défaut), le widget placé sur `x=5` `y=5` est placé dans le coin inférieur droit de la fenêtre. `x=0` `y=5` se trouve dans le coin inférieur gauche, `x=5` `y=0` se trouve dans le coin supérieur droit. À partir de là, vous pouvez décider de placer les widgets sur la grille avec précision.

Un widget peut utiliser plusieurs colonnes et / ou lignes sur cette grille. Par exemple, si vous voulez avoir un grand champ de texte prenant 2 colonnes et 3 lignes de cette fenêtre, vous pouvez faire quelque chose comme ceci :

    <text x=2 y=1 width=2 height=3 multiline>...</text>

`width` et `height` sont des attributs facultatifs sur la plupart des widgets. Ils indiquent à quel point vous souhaitez étirer ce widget horizontalement et verticalement. Ainsi, dans ce cas, le coin supérieur gauche de la zone de texte est `x=2` `y=1`, mais le widget s'étend sur deux colonnes et trois lignes. Ainsi, son coin supérieur droit est `x=3` `y=1`. Son coin inférieur gauche est `x=2` `y=4` et son coin inférieur droit est `x=3` `y=4`.

Placer les widgets de cette façon peut nécessiter un peu d'entraînement. Dessiner le design ainsi est flexible et facile à étendre, sans être trop abstrait. Si nécessaire, dessinez une grille simple sur une feuille avec 6 colonnes et 6 lignes et placez-y vos widgets, sachant qu'ils peuvent s'étendre dans l'une ou les deux directions.

## Identifiants de widget

Un dernier concept sur le widget doit être maîtrisé avant de passer à la section suivante. Les widgets peuvent avoir des identifiants (spécifiés dans l'attribut `id` de la balise du widget). Cet identifiant aidera à récupérer le widget dans le code.

      <text x=3 y=3 id=action>Action</text>

Ce widget `text` a "action" comme identifiant.

Les identifiants doivent être uniques : deux widgets ne doivent pas avoir le même. Dans certains cas, BUI déduira l'identifiant si vous ne le spécifiez pas. Cela peut être utile pour certains widgets (éléments de menu ou boutons, par exemple), mais cela peut également conduire à des situations inattendues. Et certains widgets ne nécessitent de toute façon pas d'identifiant

> Comment savoir quand utiliser les identifiants et quand ne pas le faire ?

La première chose à faire est de lire la documentation de la balise. Elle fournit quelques exemples et explique généralement pourquoi l'attribut `id` est nécessaire, pourquoi il ne l'est pas ou pourquoi il peut être déduit par BUI s'il n'est pas spécifié. Si vous êtes un concepteur graphique, la règle de base est de placer des identifiants explicites sur les widgets avec lesquels l'utilisateur va interagir (boutons, tableaux, cases à cocher...).

## Et maintenant ?

Maintenant que vous avez une meilleure compréhension du design dans BUI, il sera plus facile de jouer avec de vraies fenêtres. Les prochains tutoriels montrent un plus grand nombre d’exemples de divers widgets dans diverses conditions. Si vous êtes un concepteur de fenêtres et que le code Python ne vous intéresse pas, vous pouvez ne lire que la première section de chaque tutoriel (qui décrit le design). La section suivante (décrivant les méthodes de contrôle) est davantage utile pour les développeurs. Toutefois, si vous êtes développeur, vous voudrez sans doute lire l'intégralité du tutoriel, ou du moins suivre ceux qui vous intéressent.

- [Utiliser les boutons](buttons.md)
- [Une fenêtre avec une barre de menu](menubar.md)
- [Gestion des raccourcis clavier](keyboard.md)
- [Cases à cocher et boutons radio](choices.md)
- [Listes et tableaux](lists.md)
- [Boîtes de dialogue](dialogs.md)
