""" 
https://www.codingame.com/training/hard/cgx-formatter

Chaînes de caractères
Expression régulière
Parsing

Chez CodinGame on aime réinventer la roue. XML, JSON etc. c’est bien mais pour un web meilleur nous avons inventé notre propre format de données textuelles (nommé CGX) pour représenter de l’information structurée.​


Voici un exemple de données structurée à la CGX :

Exemple de contenu CGX formaté.
 

Représentation graphique de l'exemple.
  

Un contenu CGX est composé d'ELEMENTs.

ELEMENT
Un ELEMENT peut être de type BLOC, TYPE_PRIMITIF ou CLE_VALEUR.

BLOC
Suite d'ELEMENTs séparés par le caractère ;
Un BLOC commence par le marqueur ( et se termine par le marqueur ).

TYPE_PRIMITIF
Un nombre, un booléen, null, ou une chaîne de caractères (entourée par le marqueur ')

CLE_VALEUR
Une chaîne de caractères séparée d'un BLOC ou d’un TYPE_PRIMITIF par le caractère =
 


Votre mission : écrire un programme capable de formater un contenu CGX pour le rendre lisible !

En dehors des règles ci-dessous, le résultat affiché ne contiendra aucun espace, tabulation ou retour chariot. Aucune autre règle ne devra être ajoutée.
Le contenu des chaînes de caractères ne doit pas être modifié.
Un BLOC commence sur sa propre ligne.
Les marqueurs de début et de fin d'un BLOC sont sur la même colonne.
Chaque ELEMENT contenu dans un BLOC est indenté de 4 espaces par rapport au marqueur de ce BLOC.
Une CLE_VALEUR commence sur sa propre ligne.
Un TYPE_PRIMITIF commence sur sa propre ligne sauf s'il est la valeur d'une CLE_VALEUR.
ENTRÉE :
Ligne 1 : Le nombre N de lignes CGX à formater
Les N lignes suivantes : Le contenu CGX. Chaque ligne contient 1000 caractères maximum. Tous les caractères sont ASCII.

SORTIE :
Le contenu CGX formaté

CONTRAINTES :
Le contenu CGX fourni sera toujours valide.
Les chaînes de caractères ne contiennent pas de caractère '
0 < N < 10000
EXEMPLE :

Entrée
4
  

     true
 
Sortie
true
 
 
Entrée
1
'spaces and    tabs'
Sortie
'spaces and    tabs'
 
 
Entrée
1
(0)
 
Sortie
(
    0
)
 
 
Entrée
1
()
Sortie
(
)
 
 
Entrée
1
(0;1;2)
Sortie
(
    0;
    1;
    2
)
 
 
Entrée
1
(('k1'=1);('k2'=2))
Sortie
(
    (
        'k1'=1
    );
    (
        'k2'=2
    )
)
 
 
Entrée
10
'users'=(('id'=10;
'name'='Serge';
'roles'=('visitor';
'moderator'
));
('id'=11;
'name'='Biales'
);
true
)
Sortie
'users'=
(
    (
        'id'=10;
        'name'='Serge';
        'roles'=
        (
            'visitor';
            'moderator'
        )
    );
    (
        'id'=11;
        'name'='Biales'
    );
    true
)
 
 
Entrée
9
( 'user'= (
    'key'='1= t(c)(';
    'valid'=false
  );
  'user'= (
    'key'=' = ; ';
    'valid'= true
  ); ()
)
Sortie
(
    'user'=
    (
        'key'='1= t(c)(';
        'valid'=false
    );
    'user'=
    (
        'key'=' = ; ';
        'valid'=true
    );
    (
    )
)
"""

# code pour tester le script hors site
entries = [
    "1",
    "(('k1'=1);('k2'=2))",
]

generator = (entry for entry in entries)


def input():
    return next(generator)


######################################

import sys
import re
def afficher(*args):
    print(*args, file=sys.stderr, flush=True)


_DEBUG_MODE = 0

# Petit compteur global
_bloc_counter = 0


def DEBUG(bloc):
    global _bloc_counter
    _bloc_counter += 1

    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREY = "\033[90m"

    indent = '  ' * bloc.depth
    afficher(f"DEBUG {indent}Bloc #{_bloc_counter} (depth={bloc.depth}, type={bloc.elem_type}) : {repr(bloc.content)}")
    
    #ajout d'un attribut au bloc
    bloc.id = _bloc_counter

r=cgxlines =""
n = int(input())
for i in range(n):
    cgxline = input()
    #afficher(list(cgxline))
    #afficher('line',i,':',cgxline)
    cgxlines += cgxline

afficher(cgxlines)
"""
cgxlines="'users'=(null;'free';('id'=10;'name'='Serge';'roles'=('visitor';'moderator'));721831;('id'=11;'name'='Biales');true)"
#cgxlines="( j lj ;   iohlh   ;  jljlj    ;  pjjj ;   ())"
cgxlines="'users'=(null;'free';('id'=10;'name'='Serge';'roles'=('visitor';'moderator')))"
cgxlines= "A;B;'C';()"
"""

class Element:
    def __init__(self, content, parent=None, elem_type=None):
        self.content = content  # Le contenu du bloc (texte entre parenthèses, par exemple)
        self.parent = parent    # spécifie le parent, utile pour faire remonter les codes des sous-bloc vers le parent
        self.elem_type = elem_type   # Type du bloc : "bloc", "cle_valeur", ou "type_primitif"
        
        if parent is None:
            self.depth  = 0
        else:
            self.depth  = parent.depth  + 1
                
        self.sub_elems = self.find_sub_elements(content)  # Définir sub_blocs automatiquement
        self.is_elementaire = len(self.sub_elems) == 0  # Définir si c'est un bloc élémentaire : INUTILE ?
        if _DEBUG_MODE: DEBUG(self)


    def __str__(self):
        # Représentation du bloc avec profondeur, nombre de sous-éléments et contenu
        indent = '  ' * self.depth  # Indentation basée sur la profondeur
        result = f"{indent}Element(type='{self.elem_type}', profondeur={self.depth}, " \
                 f"nb_subs={len(self.sub_elems)}, content={self.content})"
        
        return result


    def print_tree(self, prefix="", is_last=True):
        # Affiche le root sans préfixe
        if self.parent is None:  # C'est le root, donc pas de └──
            afficher('ROOT =', self.content)
        else:
            # Affiche les sous-blocs avec les préfixes
            connector = "└── " if is_last else "├── "
            
            if self.elem_type == 'key_value_pair': # cas particulier ou le content est la paire[key,value]
                afficher(prefix + connector + self.content[0]+'='+self.content[1])
            elif self.elem_type == 'key_value':     # cas particulier de la KV sans TP
                afficher(prefix + connector + self.content+'=')
            else:
                afficher(prefix + connector + self.content)

        # Affiche les sous-blocs avec une indentation supplémentaire
        if self.sub_elems:
            for i, sub in enumerate(self.sub_elems):
                is_last_sub = (i == len(self.sub_elems) - 1)
                # Si c'est le premier niveau, on ne met pas d'indentation avant les sous-blocs
                if self.parent is None:
                    new_prefix = prefix  # Pas de décalage pour les sous-blocs du root
                else:
                    new_prefix = prefix + ("│   " if not is_last else "    ")  # Début de l'indentation pour les autres sous-blocs
                sub.print_tree(new_prefix, is_last_sub)

    def find_sub_elements(self, content):
        # Si l'élément est de type non_bloc, on retourne directement une liste vide
        if self.elem_type not in [None,'bloc'] :
            return []

        stack_paren = []  # Pile pour gérer les parenthèses
        stack_quote = []  # Pile pour gérer les guillemets
        between_quotes = False #Booléens pour ne pas stacker les () dans des guillemets dans d'autres ()
        elems = []  # Liste pour stocker les sous-blocs trouvés
        start_idx_paren = None  # L'index de début pour les parenthèses
        start_idx_quote = None  # L'index de début pour les guillemets
        non_bloc_content = ""  # Contenu temporaire pour les non-blocs
        i = 0 if self.elem_type == None else 1  # si bloc : Initialiser l'index à 1 pour sauter la ( ouvrante
        end_i = len(content) if self.elem_type == None else len(content) -1  # si bloc : Terminer l'index à 1 pour sauter la ) fermante

        while i < end_i: #on s'arrête avant le dernier caractère pour échapper la ) fermante
            char = content[i]
            # Gestion des parenthèses => BLOC
            
            if char == '(' and not stack_quote and not between_quotes:  #on s'assure qu'on est pas dans un ' '
                # Si un texte sans ' ' est en cours et on entre dans un bloc, on le crée avant de commencer un bloc
                #if non_bloc_content.strip()==';' : non_bloc_content = "" #on skip si c'est uniquement un ;
                
                if non_bloc_content.strip() : # and non_bloc_content.replace(" ", "")!=";" and non_bloc_content.replace(" ", "")!=";;" :
                    
                    afficher('NBC=', non_bloc_content)

                    if non_bloc_content.replace(" ", "")==";" : #purge les ; seuls
                        non_bloc_content = ""
                    else:    

                        if non_bloc_content[-1]==';' : non_bloc_content = non_bloc_content[:-1] #on supprime le ; si il est en bout de chaîne
                        
                        new_non_bloc = Element(non_bloc_content.strip(), parent=self, elem_type="non_quoted")
                        afficher("creation d un sub-pas'' avant ( avec", non_bloc_content)
                        elems.append(new_non_bloc)
                        non_bloc_content = ""  # Réinitialiser le contenu du non_bloc


                if not stack_paren : start_idx_paren = i       #mémoriser début du bloc

                stack_paren.append(char)  # Ouvrir une parenthèse
                #afficher('trouve (, stack=', stack_paren)
                
                

            elif char == ')' and not stack_quote and not between_quotes:  #on s'assure qu'on est pas dans un ' '
                #afficher('trouve ), stack avant pop=', stack_paren)
                stack_paren.pop()  # Fermeture de la parenthèse
                #afficher('trouve ), stack après pop=', stack_paren)
                if not stack_paren:  # Si la pile est vide, le bloc est complet
                    bloc_content = content[start_idx_paren:i+1]  # Contenu sans les parenthèses
                    new_bloc = Element(bloc_content, parent=self, elem_type="bloc")  # Créer un sous-bloc
                    #afficher('creation d un sub-bloc avec', bloc_content)
                    elems.append(new_bloc)  # Ajouter le sous-bloc à la liste
                       

            # Gestion des guillemets

            elif char =="'" and len(stack_paren) > 0 : #cas piégeux de () dans des guillemets dans des ():
                between_quotes = not between_quotes #change d'état à chaque '

            elif char == "'" and not stack_paren : # on s'assure qu'on est pas déjà dans un bloc
                
                # Si un texte sans ' ' est en cours et on entre dans un ' ', on le crée avant de commencer un bloc
                #if non_bloc_content.strip()==';' : non_bloc_content = "" #on skip si c'est uniquement un ;
                if non_bloc_content.strip() :

                    if non_bloc_content.replace(" ", "")==";" : #purge les ; seuls
                        non_bloc_content = ""
                    else: 


                        if non_bloc_content[-1]==';' : non_bloc_content = non_bloc_content[:-1] #on supprime le ; si il est en bout de chaîne
                        new_non_bloc = Element(non_bloc_content.strip(), parent=self, elem_type="non_quoted")
                        #afficher("creation d un sub-pas'' avant ' avec", non_bloc_content)
                        elems.append(new_non_bloc)
                        non_bloc_content = ""  # Réinitialiser le contenu du non_bloc
                
                if not stack_quote:  # Si c'est le premier guillemet, marquer le début
                    #afficher("1er ' en",i)
                    stack_quote.append(char)
                    start_idx_quote = i

                else:  # Si on trouve un guillemet fermant
                    #afficher("2eme ' en", i)
                    stack_quote.pop()  # Fermer le guillemet
                    # Une fois le guillemet fermé, on crée un élément
                    
                    #on vérifie si c'est le cas d'une CLE_VALEUR associé à TYPE_PRIMITIF

                    #if i < end_i -2:                                                                          
                    #    if content[i+1]=='=' and content[i+2]== "'" :
                    #        stack_quote.append("'")
                    #        i+=2
                    
                    
                    

                    if not stack_quote:

                        j, type_primitif, elem_type = self.find_key_value_pair(content[i+1:]) #renvoie le décalage éventuel pour reprendre le scan au bon endroit, le content et précise si c'est une paire clé + valeur ou une clé seule

                        #afficher(j, type_primitif, elem_type)

                        if elem_type == 'quoted':    #rien à ajouter
                            non_bloc_content = content[start_idx_quote + 1:i]  # type: ignore # Contenu sans les guillemets
                        elif elem_type == 'key_value' :     #clé sans type primitif
                            #afficher('ajout d une CLE VALEUR <',content[start_idx_quote + 1:i],'>' )
                            non_bloc_content = content[start_idx_quote + 1:i]  # type: ignore # Contenu sans la () ni le =
                        elif elem_type == 'key_value_pair' : #clé + type primitif
                            #afficher('clé=', content[start_idx_quote + 1:i])
                            non_bloc_content = [content[start_idx_quote + 1:i] ,  type_primitif] # type: ignore

                        i+=j #calcule le décalage à pratiquer si besoin

                        new_non_bloc = Element(non_bloc_content, parent=self, elem_type=elem_type)
                        
                        #afficher("creation d un sub-'' avec", non_bloc_content)
                        elems.append(new_non_bloc)
                        non_bloc_content = ""  # Réinitialiser le contenu
                        


            # Si ce n'est ni une parenthèse ouvrante ni fermante ni un guillemet, et on n'est pas dans un bloc
            
            elif char not in [';','\n', '\t'] and not stack_quote and not stack_paren :
                non_bloc_content += char  # Ajouter le caractère au contenu non_bloc
                if non_bloc_content[0]==';' : non_bloc_content = '' #on skip les ; si en début de chaîne
                #afficher('ajoute', char)
                #afficher('hors bloc, stack=', stack_paren)

            # Lorsqu'on termine un "mot" non_bloc (espace, tabulation, ou nouvelle ligne) sauf si un guillemet ou un bloc est ouvert
            elif char in [';', '\n'] and non_bloc_content.strip() and not stack_quote and not stack_paren:
                if non_bloc_content[-1]==';' : non_bloc_content = non_bloc_content[:-1] #on supprime le ; si il est en bout de chaîne
                
                new_non_bloc = Element(non_bloc_content.strip(), parent=self, elem_type="non_quoted")
                #afficher("creation d un sub-pas'' avec", non_bloc_content)
                elems.append(new_non_bloc)
                non_bloc_content = ""  # Réinitialiser le tampon

            i += 1

        # Si à la fin il reste du contenu non_bloc non traité
        if non_bloc_content.strip() : # and non_bloc_content.replace(" ","")!=';' and non_bloc_content.replace(" ","")!=';;':
            if non_bloc_content[-1]==';' : non_bloc_content = non_bloc_content[:-1] #on supprime le ; si il est en bout de chaîne
            new_non_bloc = Element(non_bloc_content.replace(" ",""), parent=self, elem_type="non_quoted")
            #afficher("creation d un sub_final avec", non_bloc_content)
            elems.append(new_non_bloc)

        return elems  # Retourner la liste d'éléments trouvés




    def find_key_value_pair(self, content) -> tuple[int, str, str]:
        #return 0, '', 'quoted'
        i = 0  
        #afficher('find KVP', content)
        while i < len(content):
            # Ignorer les espaces blancs avant le =
            if content[i].isspace():
                i += 1
                continue
            
            if content[i] == ';': return 0, '', 'quoted' # si on trouve un ;
            
            if content[i] == '=':  # Si on trouve un signe égal
                #afficher('= trouvé en',i)
                i += 1  # Passer à la valeur après le =
                while content[i].isspace(): #Ignorer les espaces blancs après le =
                    i += 1
                
                # 3 cas possibles : on tombe sur un 'type_primitif' quoted ou non ou un (bloc) 
                # Gérer les guillemets pour la valeur (si présents)
                
                if content[i] == "(":     # cas du KV avec bloc
                    return i, '', 'key_value'
                
                elif content[i] == "'":   # cas du KVP avec TP quoted
                    #afficher("' trouvé en",i)
                    start_idx = i
                    i+=1 #on se positionne dans le ' '
                    while i < len(content) and content[i] != "'":
                        i += 1  # Avancer jusqu'au guillemet fermant
                    
                    #afficher("' trouvé en",i)
                    value = content[start_idx:i+1]  # Valeur avec guillemets pour différencier les TP quoted ou non
                    #afficher('value =', value)
                    return i+1, value, 'key_value_pair'
                
                else:         # cas du TP non quoted
                    start_idx = i
                    #afficher('cas du TP non quoted, start =',i, content[i])
                    while i < len(content) and content[i] not in [ '\n', '\t', ';' , ')']:
                        i += 1 #avancer jusqu'à la fin du TP
                    #afficher('cas du TP non quoted, start =',start_idx, content[i])
                    #afficher('création de la KVP avec value =',content[start_idx:i] )
                    #afficher('value créé jusqu à l indice',i, ':', content[i])   
                    value = content[start_idx:i]  
                    #afficher(value)
                    return i, value.replace(" ",""), 'key_value_pair'

                

                 

            else:
                i += 1  # Continuer à chercher un =
                
        return 0, '', 'quoted'   #si on ne trouve pas de = c'est qu'on est tombé sur un type_primitif quoted

    def generate_code(self, prefixe='', is_last = None): # 
        """
        prefixe sert à gérer l'indentation : ' '*4 à chaque bloc
        is_last sert à gérer les ; au milieu des subs (sauf dernier)
        """
        
        
        
        code=''
        for idx, elem in enumerate(self.sub_elems):
            is_last = True if idx == len(self.sub_elems)-1 else False
            
            
            if elem.elem_type=='bloc':
                
                pattern = r"\( *\)"
                
                #afficher('génère code pour', elem.elem_type, 'is_last',is_last)
                
                if bool(re.fullmatch(pattern, elem.content)): 
                    
                    code += prefixe+'(\n'+prefixe+')' #cas particulier du bloc vide ou composé d'espaces
                    return code
                
                code += prefixe+'(\n'
                #afficher('code ( avec prefixe longueur=', len(prefixe))
                new_prefixe = prefixe + ' '*4
                code+=elem.generate_code(prefixe=new_prefixe, is_last=is_last)
                code +='\n'+  prefixe+')' +';\n'*(not is_last)
                

            elif elem.elem_type=='quoted':
                code+=prefixe + "'"+elem.content+"'"+';\n'*(not is_last)
            
            elif elem.elem_type=='non_quoted':
                for idx, e in enumerate(elem.content.split(";")):
                    code+= prefixe + e +';\n'*(idx<len(elem.content.split(";"))-1)
                    if not is_last : code+=';\n'
            
            elif elem.elem_type=='key_value':
                code+=prefixe + "'"+elem.content+"'="+'\n'*(not is_last)
            
            elif elem.elem_type=='key_value_pair':
                code+=prefixe + "'"+elem.content[0]+"'="+elem.content[1]+';\n'*(not is_last)
            
            #afficher('code intermédiaire = \n'+code)
        return code


            
 


ROOT = Element(cgxlines)

#for elem in ROOT.sub_elems:
#    afficher(elem)


ROOT.print_tree()
code = ROOT.generate_code()
afficher('Result :')
#afficher(code)
#print(len(code.split('\n')))
print(code)

