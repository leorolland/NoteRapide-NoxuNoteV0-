# encoding=utf8
import sys
import pdfkit

dico = {
	'->' : "→",
	'-->' : "→",
	'<-' : "←",
	'<--' : "←",
	':N' : "ℕ",
	':C' : "ℂ",
	':R' : "ℝ",
	':Z' : "ℤ",
	':Q' : "ℚ",
	':H' : "ℍ",
	':P' : "ℙ",
	':alpha' : "α",
	':beta' : "β",
	':gamma' : "γ",
	':Gamma' : "Γ",
	':delta' : "δ",
	':Delta' : "Δ",
	':epsilon' : "ε",
	':zeta' : "ζ",
	':eta' : "η",
	':alpha' : "α",
	':theta' : "θ",
	':Theta' : "Θ",
	':Theta' : "Θ",
	':iota' : 'ι',
	':lambda' : 'λ',
	':Lambda' : 'Λ',
	':mu' : 'μ',
	':nu' : 'ν',
	':pi' : 'π',
	':Pi' : 'Π',
	':rho' : 'ρ',
	':sigma' : 'σ',
	':Sigma' : "Σ",
	':tau' : "τ",
	':upsilon' : "υ",
	':phi' : "φ",
	':Phi' : "Φ",
	':chi' : "χ",
	':psi' : "ψ",
	':Psi' : "Ψ",
	':omega' : "ω",
	':Omega' : "Ω",
	':perp' : "⊥",
	'1/2' : "½",
	'1/3' : "¼",
	'+-' : "±",
	'^2' : "²",
	'^3' : "³",
	':x' : "×",
	':pourtout' : "∀",
	':ilexiste' : "∃",
	':appartient' : "∈",
	':appartienta' : "∈",
	':appartientpas' : "∉",
	':appartientpasa' : "∉",
	':nappartientpas' : "∉",
	':nappartientpasa' : "∉",
	':ensemblevide' : "∅",
	':contient' : "∋",
	':produit' : '<font size="6em">∏</font>',
	':somme' : '<font size="6em">∑</font>',
	':-' : "−",
	':racine' : "√",
	':racinecarree' : "√",
	':infini' : "∞",
	':inter' : "∩",
	':union' : "∪",
	':integrale' : '<font size="6em">∫</font>',
	'~=' : "≈",
	'=~' : "≈",
	'!=' : "≠",
	':different' : "≠",
	':nonégal' : "≠",
	'<=' : "≤",
	'>=' : "≥",
	':point' : "⋅",
}

# On ouvre la note
name = sys.argv[1]
fichier = "/Users/blacky/Documents/cours/notes/nt_"+name+".txt"
note = open(fichier, "r", encoding='utf-8').read()

# On remplace les mots du texte par ceux du dictionnaire
for i in dico:
	note = note.replace(i, dico[i])

# Si on veux rendre en manuscrit, on lit la première ligne et on définit la variable
manuscrit = False
if note[0:9] == "manuscrit":
	manuscrit = True
	note = note[10:] # On supprime le mot

# Mise en gras et souligné
gras = False
souligne = False
noterecompose = ""
for lettre in note:
	if lettre == "*":
		if not gras:
			noterecompose+="<b>"
			gras = True
		else:
			noterecompose+='</b>'
			gras = False
	elif lettre == "_":
		if not souligne:
			noterecompose+="<u>"
			souligne = True
		else:
			noterecompose+='</u>'
			souligne = False
	else:
		noterecompose+=lettre
note = noterecompose

# Si problèmes de lectures, importer 'io' et remplacer par :
# with io.open("note.txt",'r',encoding='utf8') as f:
#     note = f.read()

# On sépare le texte en un tableau représentant chaque ligne
lines = note.split('\n')

# On définit l'HTML de base, comprenant le style et le charset pour les accents
html = """
<meta charset="utf-8">
<style type = "text/css">
	@font-face {
		font-family: "Manuscrit";
		src: url('GastonDemo.otf');
	}
	body {
		max-width: 1000px;
		font-family: Helvetica, Arial, sans-serif;
		font-size: 1.1em;
		color: #002259;
		line-height: 160%;
	}
	div#liste {
		margin-left: 60px;
	}
	div#texte {
		margin-left: 30px;
	}
	h2 {
		text-decoration : underline;
		margin-bot: -10px;
	}
	h1 {
		border-bottom: 2px solid #CC0000;
		padding-bottom: 12px;
    	line-height: 200%;
	}
	table
	{
	    border-collapse: collapse;
	    margin-left: auto;
	    margin-right: auto;
	}
	td
	{
		padding: 5px;
	    border: 1px solid black;
	}
</style>
"""

# Si on avait défini manuscrit auparavant, on change la police d'écriture principale
if manuscrit:
	html+='<style>body { font-family: "Manuscrit", Helvetica, Arial, sans-serif; }</style>'

# Si sauterligne=True on saute la ligne et on passe à la suivante
sauterligne = False 

# Si la ligne d'avant était aussi un tableau
LigneAvTableau = False

# Pour chaque ligne du document
for index, line in enumerate(lines):

	# Si sauterligne=True on saute la ligne et on passe à la suivante
	if sauterligne == True:
		sauterligne = False
		continue

	# Petit titre
	if line[0:2] == "# ":
		# On écrit l'HTML
		html+="<h3> %s </h3>"%(line.replace("#",''))

		# S'il y a une ligne vide après, on la saute
		try:
			if lines[index+1] == "":
				sauterligne = True
		except:
			pass

	# Moyen titre
	elif line[0:3] == "## ":
		# On écrit l'HTML
		html+="<h2> %s </h2>"%(line.replace("#",''))

		# S'il y a une ligne vide après, on la saute
		try:
			if lines[index+1] == "":
				sauterligne = True
		except:
			pass

	# Grand titre
	elif line[0:4] == "### ":
		# On écrit l'HTML
		html+="<center><h1> %s </h1></center><br>"%(line.replace("#",''))

		# S'il y a une ligne vide après, on la saute
		try:
			if lines[index+1] == "":
				sauterligne = True
		except:
			pass

	# Attention/Remarque
	elif line[0:3] == "/!\\":
		# On écrit l'HTML
		html+='<div id="texte"><img src="attention.png", height=24></img><font color="#BB0000"><b>%s</b></font></div>'%(line[2:])
	elif line[0:2] == "! ":
		# On écrit l'HTML
		html+='<div id="texte"><img src="attention.png", height=24></img><font color="#BB0000"><b>%s</b></font></div>'%(line[1:])

	# Liste d'éléments
	elif line[0:1] == "-":
		# On écrit l'HTML
		html+='<div id="liste">&#149; %s</div>'%(line[1:])

	# Saut de ligne
	elif line[0:2] == "":
		html+="<br>"

	# Tableau
	elif line[0]=="|":

		# On ouvre la balise tableau si c'est la première ligne
		if not LigneAvTableau:
			html+="<table>"
			LigneAvTableau = True
		
		# On ajoute une ligne au tableau
		html+="<tr>"

		# On ajoute une colonne pour chaque élément
		for colonne in line[1:-1].split("|"):
			html+="<td>"+colonne+"</td>"

		# On ferme la ligne
		html+="</tr>"

		# On ferme la balise tableau si la ligne d'après n'est pas un tableau
		try:
			if not lines[index+1][0:1] == "|":
				LigneAvTableau = False
				html+="</table>"
		except:
			html+="</table>"

	# Texte encadré
	elif line[0]=="[":

		# On crée un tableau d'une seule ligne et une seule entrée
		html+="<table><tr><td>"
		html+=line[1:]
		html+="</table></tr></td>"

	# Texte
	else:
		html+='<div id="texte">%s</div>'%(line)

# On crée le fichier HTML
open("parsed.html", "w", encoding='utf-8').write(html)

# On crée le fichier pdf à partir de l'HTML
options = {
    'page-size': 'A4',
    'margin-top': '1.8cm',
    'margin-right': '1.8cm',
    'margin-bottom': '1.8cm',
    'margin-left': '1.8cm',
    'encoding': "UTF-8",
    'zoom': 2.5,
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
}

pdfkit.from_file('parsed.html', '/Users/blacky/Documents/cours/pdfs/%s.pdf'%(name), options=options)