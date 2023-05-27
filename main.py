import sys, random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Jeu(QWidget):
    def __init__(self):
        super().__init__()

        # Déclaration des variables
        self.titre = "Trouvez le mot"
        self.x = 50
        self.y = 50
        self.largeur = 600
        self.hauteur = 500
        self.icone = "images/Python.png"
        self.ligneCourrante = 0
        self.motATrouver = " "
        self.initTableau()

    def initTableau(self): # Création de la fenêtre de jeu (7 lignes x 6 colonnes)
        self.setGeometry(self.x, self.y, self.largeur, self.hauteur)
        self.setWindowTitle(self.titre)
        self.setWindowIcon(QIcon(self.icone))
        self.getMotHazard()
        grid = QGridLayout()
        grid.setRowMinimumHeight(0,30)
        grid.setRowMinimumHeight(7,30)
        grid.setColumnMinimumWidth(0,30)
        grid.setColumnMinimumWidth(6,30)
        self.setStyleSheet("""
        background: #FFFFFF;
        """)
        self.setLayout(grid)

        # Titre dans la fenêtre du jeu
        self.labelTitre = QLabel("Trouvez le mot")
        self.labelTitre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
        font-size: 40px;
        font-weight: bold;
        font-family: 'Comic Sans MS';
        margin: 30px 30px 30px 30px;
        """)
        grid.addWidget(self.labelTitre, 0, 0, 1, 7)

        # Création des boites pour les lettres de l'utilisateur
        # tableau de tableau pour chaque ligne de boites : [ [], [], [], [], [] ].
        self.boiteTexteUtil = [[] for _ in range(5)]

        # tuples des coordonnées pour chaque boite sur chaque ligne :[(1, 1), (1, 2), (1, 3), (1, 4), ..., (5, 5)].
        positions = [(i + 1, j + 1) for i in range(5) for j in range(5)]
        for i, position in enumerate(positions):
            self.boiteTexteUtil[position[0]-1].append(QLineEdit())
            grid.addWidget(self.boiteTexteUtil[position[0]-1][position[1]-1],*position) # (*) permet de passer le tuple 'position' en paramètre

        # dimensions et style des boites pour les lettres de l'utilisateur
        for i, ligne in enumerate(self.boiteTexteUtil):
            for lettre in ligne:
                lettre.setMaxLength(1)
                lettre.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lettre.setMinimumWidth(100)
                lettre.setMinimumHeight(100)
                lettre.setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                margin: 10px 10px 10px 10px;
                font-size: 36px;
                background: #FFFFFF;
                """)
                # style différent si ce n'est pas la ligne courrante
                if i != self.ligneCourrante:
                    lettre.setReadOnly(True)
                    lettre.setStyleSheet("""
                    border: 2px solid #000000;
                    border-radius: 10px;
                    margin: 10px 10px 10px 10px;
                    font-size: 30px;
                    background: #D3D3D3;
                    """)

        # Message pour l'utilisateur
        self.messageUtilisateur = QLabel(" ")
        self.messageUtilisateur.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.messageUtilisateur.setStyleSheet("""
        font-size: 20px;
        """)
        grid.addWidget(self.messageUtilisateur, 7, 0, 1, 7)

        # Création du bouton recommencer
        self.btnRecommencer = QPushButton("Recommencer")
        self.btnRecommencer.setStyleSheet("""
        *{
        border: 2px solid #000000;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        margin: 0px 0px 30px 0px;
        color: #000000;
        background: #FF0000;
        }
        *:hover{
        color: #FFFFFF;
        background: #8B0000;
        }
        """)
        self.btnRecommencer.clicked.connect(self.btnRecommencerClicked)
        grid.addWidget(self.btnRecommencer, 8, 2, 1, 3)
        self.btnRecommencer.hide()

        # Création du bouton deviner
        self.btnDeviner = QPushButton("Deviner")
        self.btnDeviner.setStyleSheet("""
        *{
        border: 2px solid #000000;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        margin: 0px 0px 30px 0px;
        color: #000000;
        background: #90EE90;
        }
        *:hover{
        color: #FFFFFF;
        background: #008000;
        }
        """)
        self.btnDeviner.clicked.connect(self.btnDevinerClicked)
        grid.addWidget(self.btnDeviner, 8, 2, 1, 3)


    def getMotHazard(self):
        listeMots = open("mots.txt", "r")
        mots = listeMots.read().splitlines()
        listeMots.close()
        self.motATrouver = random.choice(mots)
        print(self.motATrouver)

    def btnRecommencerClicked(self):
        self.getMotHazard()
        self.ligneCourrante = 0
        self.messageUtilisateur.setText("")
        for i, ligne in enumerate(self.boiteTexteUtil):
            for lettre in ligne:
                lettre.setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 36px;
                background: #FFFFFF;
                margin: 10px 10px 10px 10px;
                """)
                lettre.setReadOnly(False)
                lettre.setText("")
                if i != self.ligneCourrante:
                    lettre.setReadOnly(True)
                    lettre.setStyleSheet("""
                    border: 2px solid #000000;
                    border-radius: 10px;
                    font-size: 36px;
                    background: #D3D3D3;
                    margin: 10px 10px 10px 10px;
                    """)
        self.changerBouttons()

    def btnDevinerClicked(self):
        if self.verifierValidite() == False: # si le caractère n'est pas une lettre
            self.messageUtilisateur.setText("Entrez seulement des lettres")
            self.messageUtilisateur.repaint()
        elif self.verifierGagnant() == False: # si le mot n'a pas encore été trouvé
            self.messageUtilisateur.setText(" ")
            self.messageUtilisateur.repaint()
            if self.ligneCourrante < 4: # si ce n'est pas la dernière chance
                self.couleurLigneActive()
                self.activerLigneSuivante()
            else:
                self.couleurLigneActive()
                self.perdu()

    def perdu(self):
        self.messageUtilisateur.setText(f"Perdu! Le mot était : {self.motATrouver}")
        self.messageUtilisateur.repaint()
        self.changerBouttons()

    def activerLigneSuivante(self):
        for i in range(5):
            self.boiteTexteUtil[self.ligneCourrante + 1][i].setStyleSheet("""
            border: 2px solid #000000;
            border-radius: 10px;
            font-size: 36px;
            margin: 10px 10px 10px 10px;
            background: #FFFFFF;
            """)
            self.boiteTexteUtil[self.ligneCourrante + 1][i].setReadOnly(False)
        self.ligneCourrante += 1

    def couleurLigneActive(self):
        for i in range(5):
            self.boiteTexteUtil[self.ligneCourrante][i].setReadOnly(True)
            caractere = self.boiteTexteUtil[self.ligneCourrante][i].text().lower()
            if caractere == self.motATrouver[i]: # lettre fait partie du mot à trouver et est à la bonne position
                self.boiteTexteUtil[self.ligneCourrante][i].setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 36px;
                margin: 10px 10px 10px 10px;
                background: #008000;
                """)
            elif caractere in self.motATrouver: # lettre fait partie du mot à trouver et est à la mauvaise position
                self.boiteTexteUtil[self.ligneCourrante][i].setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 36px;
                margin: 10px 10px 10px 10px;
                background: #FFFF00;
                """)
            else: # lettre ne fait pas partie du mot à trouver
                self.boiteTexteUtil[self.ligneCourrante][i].setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 36px;
                margin: 10px 10px 10px 10px;
                background: #A9A9A9;
                """)

    def verifierGagnant(self): # vérification si la partie est gagnée
        gagne = False
        ligneMotCourrant = ""
        for i in self.boiteTexteUtil[self.ligneCourrante]:
            ligneMotCourrant += i.text() # construit un mot avec les lettres de la ligne entrées par l'utilisateur

        if ligneMotCourrant == self.motATrouver: # vérifie si le mot a été trouvé
            gagne = True
            for i in self.boiteTexteUtil[self.ligneCourrante]:
                i.setStyleSheet("""
                border: 2px solid #000000;
                border-radius: 10px;
                font-size: 36px;
                margin: 10px 10px 10px 10px;
                background: #008000;
                """)
                i.setReadOnly(True)
            self.messageUtilisateur.setText("Gagnant!")
            self.messageUtilisateur.repaint()
            self.changerBouttons()
        return gagne

    def changerBouttons(self):
        if self.btnDeviner.isVisible():
            self.btnDeviner.hide()
            self.btnRecommencer.show()
        else:
            self.btnRecommencer.hide()
            self.btnDeviner.show()

    def verifierValidite(self):
        valide = True
        for i in self.boiteTexteUtil[self.ligneCourrante]:
            if i.text().isalpha() == False:
                valide = False
        return valide

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Jeu()
    ex.show()
    sys.exit(app.exec())


