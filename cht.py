import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
        "Donnez-moi un résumé du rapport ",
        "Quels sont les objectifs principaux de la mobilisation du foncier public pour l'investissement en 2025 ?",
        "Quels sont les critères utilisés pour sélectionner les terrains publics destinés à l'investissement ?",
        "Quels défis sont identifiés dans la gestion et la mobilisation du foncier public pour l'investissement ?",
        "Quelles sont les mesures prévues pour optimiser l’utilisation du foncier public dans le cadre de ce projet ?"]    

# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()
def main():
    text="""
    
RAPPORT SUR LE FONCIER PUBLIC MOBI E POUR L’INVESTISSEMENT

INTRODUCTION

La Direction des Domaines de l'Etat, en tant qu’agent foncier de l’'Etat, contribue
activement au développement socio-économique du pays. Elle vise, à travers la

mobilisation du foncier privé de l’Etat, les objectifs suivants :

> Donner une impulsion aux politiques d’investissement productif et aux stratégies

sectorielles de l’Etat ;
>  Contribuer au développement des équipements publics et des services sociaux ;

>  Accompagner la réalisation des projets de l’'Habitat Social et le recasement des
bidonvilles.
Depuis l’année 2002, date de la déconcentration de l’Investissement et la création
des Centres Régionaux d'Investissement, le patrimoine foncier de l'Etat a été
fortement sollicité pour la promotion de l’investissement privé, ainsi que pour |les
stratégies sectorielles créatrices de richesses et des emplois.

De ce fait, le foncier de l'Etat (Domaine Privé) constitue un levier pour le soutien et
la promotion des investissements productifs. En effet, durant les 4 dernières années,
la Direction des Domaines de l’Etat a mobilisé (hors partenariat agricole) près de
1622.1444 Ha couvrant l’essentiel des chantiers de mise à niveau des infrastructures
de base et des grands projets de développement pour un investissement global
projeté de l’ordre de 91527 MMdh permettant la création de 120.935 emplois

escomptés.

Le présent rapport. préparé par la Direction des Domaines de l’Etat, conformément
aux dispositions de la loi organique n°130-13 relative à la loi de finances, dresse le
bilan de la mobilisation, pour investissement, du patrimoine foncier de l’Etat au titre

des exercices 2023 et 2024 (1°" semestre).



CHAPITRE !: MOBILISATION DU DOMAINE PRIVE DE
L’ETAT AU TITRE DE L’EXERCICE 2023

|. MOBILISATION DU FONCIER AU PROFIT DE L’INVESTISSEMENT
(HORS PARTENARIAT AGRICOLE)

La mobilisation du DPE est effectuée conformément aux dispositions de l’article
82 du décret Royal n°330-66 du 21 avril 1967 portant règlement général de la
comptabilité publique, tel qu’il a été complété et modifié, du décret relatif aux
attribputions du ministère de l’économie et des finances, et de l’arrêté n°367-02
portant délégation de pouvoirs aux walis des régions, et ce par le biais des
autorisations de cession ou de location des terrains relevant du domaine privé de
l'Etat.

Les modalités de traitement et d'approbation des demandes de cession et/ou de
location des terrains du DPE pour la réalisation des projets d’investissement, sont
accomplies conformément aux dispositions de la Loi 4718 « portant Réforme des
Centres Régionaux … d'Investissementet création des Commissions Régionales
Unifiées d'Investissement», considérés désormais comme |les seuls organes de
décision et de coordination de l’action des administrations compétentes en matière

d’investissement au niveau déconcentré.

1. Données globales

Dans le cadre des dispositions législatives et réglementaires encadrant la Gestion
Déconcentrée de l'Investissement, les Centres Régionaux d'Investissement (CRI) ont
procédé, à travers «la Commission Régionale Unifiée d'Investissement », de concert
avec les services extérieurs de la Direction des Domaines de l’Etat, à l'examen de
plusieurs projets d'investissement ayant pour support des terrains relevant du
Domaine Privé de l’Etat, situés dans diverses régions du Royaume.

A cet égard, 466 projets, ayant pour support un foncier domanial, ont été approuvés,
au titre de l’exercice 2023, pour une superficie globale de l’ordre de 13.438 Ha et un
investissement projeté de plus de 37.830 Mdh permettant la création de 20.474

postes d’emploi.

yN



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

Dakhla-Oued Eddahab 248 1.120ha 21a 13ca 5.048.025.000 6.281
Laâyoune-Sakia El Hamra 99 1.845ha O7a 10ca 21.960.122.000 277
Tanger-Tétouan-AI Hoccima 29 289ha 27a 27ca 8.165.022.000 4.621
Guelmim-Oued Noun 15 72ha 82a 58ca 432.404.319 551
Rabat-Salé-Kénitra 8 37ha 73a 85ca 325.332 917 2.651
Casablanca-Settat 12 29ha 86a 89ca 656.914.740 1116
L'Oriental 43 26ha 55a O9ca 867.907.600 1997
Marrakech-Safi 3 O6ha 99a O3ca 99.770.000 124
Souss-Massa 5 O6ha Sla 63ca 135.060.000 210
Fès-Meknès 1 O2ha 37a O9ca 20.000.000 30
Deraa-Tafilalet 1 OOha 38a 24ca 98.000.000 84

Béni Mellal-Khénifra 2 OOha s6a 84ca 21.71/.545 ©s

2.Ventilation par Mode de mobilisation du Foncier

Dans le cadre de l’optimisation de l’allocation du foncier mobilisé au profit de
l’investissement, l’Etat (Domaine Privé) adopte une stratégie visant, entre autres, la
valorisation de sa réserve foncière moyennant la normalisation et la diversification
du mode de mobilisation du foncier, suivant la nature et la vocation du projet
d’investissement (Industriel, Habitat, Tourisme, Energie …).

Ainsi, et dans le cadre de l’allocation rationnelle du foncier domanial, en fonction de
la dimension et de la portée des projets d’investissement, la Direction des Domaines
de l’Etat privilégie l’option de la mobilisation du foncier par voie de location, destiné

à abriter les grands projets nécessitant des assiettes foncières très étendues.

Cette  normalisation a pour objectif,  d’éviter la mobilisation de … superficie
surdimensionnée par rapport à la portée des projets à réaliser.

De même, et afin d’encourager les investissements et réduire le coût du foncier
destiné à recevoir les projets dans le secteur Industriel, l’'Etat (Domaine Privé)

privilégie la voie de la mobilisation, par location, des lots des Zones Industrielles

aménagées au profit des investisseurs.

L É


> Ainsi, l’Etat (Domaine Privé) a mobilisé, par voie de location, presque 84% du

foncier domanial octroyé au cours de l’année 2023.

Superficie allouée/Mode de mobilisation

Location _83.94D/°
Cession - 16,04%

Cession et location _ 0,02%

> 94% de cette superficie mobilisée, par voie de location, est destinée à recevoir

des projets dans les secteurs de l’Energie et des Mines.

Superticie mobilisée par voie de location/Secteur
d'activité

Industrie ' 2,40%
Agro-industrie l 180%
Tourisme l 0.66%
Habitat | 0.65%
Services | 0,48%
Sporl | 0,99%

Enseignement et Formation | 0,02%

Santé 0,01%

pN



E POUR L’INVESTISSEMENT

3. Ventilation par secteur d'activité
Sur le plan sectoriel, la ventilation des projets approuvés au titre de l’année 2023 fait
ressortir les constats suivants :

>  La ventilation par secteur d'’activité fait ressortir qu’environ 75% des projets

sont concentrés au niveau de quatre secteurs d'activité (Tourisme, Industrie,

Services et Agro-Industrie).

Nb projets/Secteur d'activité

Tourisme E 25.752
\ndustrie E 20.17
Services E 15.055
Agro-industrie EN 11 570
Habitat E 8.80 %
Mines E 7519
Enseignement et Formation NNN 3,43%
Sport I 1.93%
Santé M 150%
Autres secteurs d'activité [ 0.86%
Energie B 0,65%

#

> La répartition du foncier mobilisé par secteur d'’activité fait ressortir que plus

À

de 83% de la superficie mobilisée, est dominée par deux secteurs d'activité :

Fnergie et Mines.

Superficie mobilisée/Secteur d'activité

Erersie E = =. =-
Mires E 20.517
Habitat NNN 6.22%
Autres secteurs d'activité IM 3.49%
Industrie M 3.36%
Agro-industrie M 167%
Tourisme } 139%
Services } 0,52%
Enseignement et Formation | 0,10%
Sport | 0,07%
Santé . 0,03%

L É



> La ventilation sectorielle des investissements fait ressortir la prédominance de
trois secteurs … d’activité (Mines, Energie et Industrie),  avec 75%  des

investissements projetés.

Investissement projeté/Secteur d'activité

Energie E 15,520.
industrie IN 11.7006
Habitat N o.50°<
Tourisme IM 6430
Agro-industrie MM 3.78%
santé I 242x
Services [} 1.63%
Enseignement et Formation | 0.45%
Sport | 0,19%

Autres secteurs d'activité | 0.08%

> La répartition des emplois générés est marquée par la forte contribution de
quatre secteurs d'activité (Industrie, Tourisme, Agro-industrie et Services),

avec 83% des postes d’emploi à créer.
Æ %
Emplois/Secteur d'activité
Agro-industrie — 10,97%
services RE o.c406
santé E 5.1
Mines ME 4155

Enseignement et Formation } 2.69%

sport M 243%

Enercie MI 1.95%

Autres secteurs d'activité | 0.34%

VN



R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

3.1 Secteur de l’Energie

L'année 2023 a enregistré l’approbation de 3 projets dans le secteur de l’'Energie,

pour une superficie globale de plus de 7.168 Ha.

Ces projets d’investissement d’une valeur globale de 5.13 Mdh correspondant à la
création, à terme, de 400 postes d’emploi, seront implantés, principalement, au
niveau de la région de Dakhla-Oued Eddahab qui totalise 98% de la superficie
globale mobilisée au profit de ce secteur, dédiée à la réalisation d'un Parc Eolien à

Dakhla d’une capacité nominale de 100 MW.

S'agissant de la ventilation régionale des projets approuvés, au titre de l’année 2023,
la région de Tanger -Tétouan- Al Hoceima a bénéficié de plus de 67% des projets
accordés en faveur de ce secteur, consistant en la réalisation d’une Centrale solaire
photovoltaïque d’une capacité nominale de 35 MW à Tanger et l’extension de la

Station Thermique de Tahadart.

Nbre Projets Superficie mobilisée

ë Tanger-Tetouan-AI
Dakhla-Oued Eddahab - 33% Hoceima l 2%

# x
/ .
Investissement projeté Emplois
Dakhla-Oued Eddahab l 5% Tanger TetoyanzAl ' 15%
Hoceima

L A



3.2 Secteur des Mines

L’Etat (Domaine Privé) a mobilisé, au titre de l’année 2023, des assiettes foncières,
d’une superficie globale de 4.006 Ha, dédiées à la réalisation de 35 projets dans le
secteur des Mines.

Ces projets d’investissement d'une valeur globale de 18.879 Mdh, devraient générer
la création, à terme, de 846 postes d’emploi.

Au cours de cette période, c’est la région de Dakhla-Oued Eddahab qui a enregistré
80,4% de la superficie globale mobilisée au profit de ce secteur.

En termes de répartition régionale des projets approuvés, au cours de cette période,
es régions de Dakhla -Oued Eddahab et de Laäyoune-Sakia El Hamra ont bénéficié

de plus de 91% des projets accordés en faveur de ce secteur.

Nbre Projets Superficie mobilisée

Laäyoune-Sakia El Hamre E 15.575s | Dethia-Ouec Eddahab —80,40%
Dakhla-Oued Eddahab — 4286% | | Laäyoune-Sakia El Hamra - 19,07%

Guelmim-Oued Noun - 8,57% Guelmim-Oued Noun | 0,53%

Investissement projeté Emplois

Laäyoune-Sakia El Hamra — 99,06% Laäyoune-Sakia El Hamra — 60,17%

Dakhla-Oued Eddahab | 0,82% Dakhls-Oued Eddatab DEN 321555

Guelmim-Qued Noun | 0.12% Guelmim-Qued Noun ' 7,68%

yN



E POUR L’INVESTISSEMENT

3.3 Secteur de l’Habitat

Au cours de l’année 2023, l’Etat (Domaine privé) a mobilisé une superficie globale de
plus de 836 Ha, au profit de 41 projets d'investissement dans le secteur de l’Habitat,
pour une enveloppe totale de 3.706 Mdh.

Plus de 99,5% de la superficie mobilisée au profit de ce secteur, est située au niveau
de deux régions : Laâäyoune-Sakia El Hamra et Dakhla -Oued Eddahab.

En se référant à la ventilation régionale des projets approuvés, au cours de cette
période, ce sont les régions de Dakhla -Oued Eddahab et de Laäyoune-Sakia El

Hamra qui ont enregistré plus de 95% des projets accordés au profit de ce secteur.

Nbre Projets Superficie mobilisée

Dakhla-Oued Eddahab Laäyoune-Sakia El Harmra - 55,05%
Läaäyoune-Sakia El Hamra - 43,90% Dakhla-Oued Eddahab - 44,48%

Tanger-Tetouan-AI Tanger-Tetouan-AI
Hoceima l 24006 Hoceima OO
Casablanca-Settat l 2,44% Casablanca-Settat _ 0.01%

Investissement projeté

Lüôyounersak;o Éreme _ S008
D- Oued Fagsnep — se

Tanger-Tetouan-AI Hoceima l 140%

Casablanca-Settat l 0,46%

L É



3.4 Secteur de l’Industrie

94 projets d’investissement dans le secteur Industriel ont bénéficié, au titre de
l’année 2023, de la mobilisation, par l’Etat (Domaine privé), d’une superficie globale
de plus de 452 Ha.

Ces projets d'investissement, d'une enveloppe globale de plus de 4460 Mdh,
devraient générer la création, à terme, de 7.981 postes d’emploi.

La quasi-totalité de la superficie mobilisée en faveur de ce secteur (Presque 94%),
est concentrée au niveau de quatre régions: Dakhla-Oued Eddahab, Laâyoune-Sakia

El Hamra, Tanger-Tétouan-El Hoceima et Rabat -Salé-Kénitra.

En termes des projets approuvés, au cours de cette période, la région de

Dakhla-Oued Eddahab a bénéficié de plus de la moitié des projets accordés en

aveur de ce secteur.
Nbre Projets Superficie mobilisée
Dakhla-Oued Eddahab D 50575 Dakhla-Oued Eddahat N 45.4556
Tanger-Tetouan-Al Hoceima } 11.70% Laäyoune-Sakis El Hamra IN 24.47%
l aâyoune-Sakia Fl Hamra I 11.70% Tanger-Tetouan-Al Hoceima I 17.82%
L'Oriental B} 7,45% Rabat-Salé-Kénitra M 8,20%
Rabat-Salé-Kénitra J 3,20% Casablanca-Settat J_ 2,69%
Marrakech-Safi } 2,13% l'oriental | 1.02%
Casablanca-Settat }} 2.13% Marrakech-Safi | 0,91%
Souss-Massa | 1,06% Guelmim-Oued Noun | 0,88%
Guelmim-Oued Noun | 106% Souss-Massa | 0,58%
P.
Investissement projeté Emplois
Tanger-Tetouan-Al Hoceima E 4 +,5 79 || _ Tanger-Tetouan-AI Hoceime NNN = 7,7406
Dakhla-Oued Eddshab I 18,26% Rabat Salé Kénitra NNN 31.552
Lasyoune-Sakia El Hamra I 15,07% Dakhla-Oued Eddahab II 12.816
Casablanca-Settat J 7.46% Laäyoune-Sakia El Hamra [ 6.75%
Rabat-Salé-Kénitra M 7.08% L'Oriental M 5,67%
L'Oriental ' 4,84% Casablanca-Settat I 3,12%
Guelmim-Oued Noun } 183% Souss-Massa | 1.00%
Souss-Massa | 1.20% Guelmim Oued Noun | 0,70%
Marrakech-Safi | 0.69% Marrakech-Safi | C.66%

VN



IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

3.5 Secteur de l’Agro-industrie

Au cours de l’année 2023, l'Etat (Domaine Privé) a mobilisé plus de 2246 Ha, au
profit de 53 projets dans le secteur de l’Agro-industrie, pour un investissement
global de 1.431 Mdh permettant la création de 2.246 postes d’emploi.

Environ 71% de la superficie mobilisée en faveur de ce secteur, est située au niveau
de la région de Dakhla-Oued Eddahab.

Au cours de cette période, les régions de Dakhla-Oued  Eddahab et de
Laâyoune-Sakia El Hamra ont bénéficié de près de 74% des proiets accordés en
aveur de ce secteur.

Nbre Projets Superficie mobilisée

Laä ne-Sakia El

aay°üaîwa à - 30,19% Guelmim-Oued Noun - 17,81%
'O Laäyoune-Sakia El
L'Oriental - 18,87% Harira l 6,85%

Guelmim-Oued Noun l 3,76% L'Oriental l 3,74%
Casablanca-Settat l1,89% Casablanca-Settat | 0,32%
Tangir{;‘£âfä:än—Al |189% TangîæïîfÊf”"“ 0.30%

%
Investissement projeté Emplois

Laäyoune-Sakia El
Dakhla-Oued Eddahab — 45,03% Hamra — 43,77%
Laâyoune-Sakia El 30,26% Dakhla-Oued Eddahab - 25,91%
Hamra 2220 ,
L'Oriental - 11,93% L'Oriental - 14,47%

Guelmim-Oued Noun - 8,94% Guelmim-Oued Noun ' 8,28%
Tanger-Tetouan-AI > Tanger-Tetouan-AI ÿ
Hoceima l 210% Éoceima l 5,34%

Casablanca-Settat l 1,74%

Casablanca-Settat l 2,23%

L É



| PROJET DE LOiDE FiNaNCES POUR L'anNeE 2025 | S
3.6 Secteur du Tourisme

Le secteur du Tourisme a bénéficié, au titre de l’année 2023, de
plus de 187 Ha, en vue de réaliser 120 projets d’investissement, ayant un capital total

de l’ordre de 2.433 Mdh correspondant à de 4.988 postes

la mobilisation de

la création, à terme,

d’emploi.
De plus, c’est la région de Dakhla-Oued Eddahab qui en a été la principale
bénéficiaire avec 67% des projets accordés, 75% de la superficie mobilisée, 45% du
montant global investi et 64% des postes d’emploi à créer au profit de ce secteur.
Nbre Projets Superficie mobilisée
Dakhla-Oucd Eddahab E 66.670 Dakhla-Oued Eddahab E 748796
Tanger-Tetouan-AI Hoceima ' 7,50% Laäyoune-Sakia El Hamra ' 8,64%
l aâyoune-Sakia Fl Hamra B 667% Tanger-Tetouan-Al Hoceima } 5,86%
Guelmim-Oued Noun } 6.67% Casablarca-Settat }} 3,79%
L'Oriental Ÿ 5,83% Guelmim-Oued Noun | 2,84%
Casablanca-Settat | 167% Marrakech-Safi | 1,51%
Souss-Massa | 187% Fès-Meknès | 127%
Marrakech-Safi | 0,83% L'Oriental | 0,66%
Fès-Meknès | 0,83% Souss-Massa _ 0,40%
Rabat-Salé-Kénitra | 0,83% Rabat-Salé-Kénitra _ 0,1%
Béni Mellal-Khénifra | 083% Béni Mellal-Khénifra  0,05%

pN

Investissement projeté Emplois
Dakhla Oed Edohot> n . 300 Dakhla-Oued Eddahab E 63,52%
Tanger-Tetouan-AI Hoceima — 26,46% Tanger-Tetouan-Al Hoceima - 14,11%
Guelmim-Oued Noun M 7.86% L'oriental [ 5,75%
Laäyoune-Sakia El Hamra M 6,03% Laäyoune-Sakis El Harmra [} 4,32%
Casablanca-Settat [ 4.99% Guelmim-Oced Noun Ÿ 4,16%
L'orientel B} 3,79% Casablanca-Settat }} 3,66%
Marrakech-safi _ 2,87% Souss-Massa | 1,47%
Souss-Massa }} 1,93% Marrakech-Safi | 1,40%
Béni Mellal-Khénifra | 0,86% Béni Mellal-Khénifra | 1%
Fès-Moknès | 0,81% Fès-Meknès | 0,60%
Rabat-Salé-Kénitra _ 0.01% Rabat-Salé-Kénitra _ 0,01%



IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

3.7 Secteur des Services

Au cours de l’année 2023, le secteur des Services a bénéficié de la mobilisation, par
l’'Etat (Domaine Privé), d’'une superficie totale de 69 Ha, au profit de 84 projets
d'investissement pour une enveloppe globale de plus de 616 Mdh correspondant à la

création de 1.850 emplois.

Environ 88% de la superficie mobilisée au profit de ce secteur, est concentrée au
niveau de Gquatre régions: Tanger-Tétouan-Al  Hoceima,  Dakhla-Oued  Eddahab,

l'Oriental et Laâäyoune -Sakia El Hamra.

Au cours de cette période, la région de Dakhla-Oued Eddahab a enregistré,
respectivement, plus de 47% des projets accordés, plus de 31% des investissements
et plus de 27% des postes à créer, en faveur de ce secteur.

Nbre Projets Superficie mobilisée
Dakt:la-Ouecd Ec> | N « 75255 Tanger-Tetouan-Al
Éccoms - ME C 1056

Laäyoune-Sakia El
Hamra E 2262> Dakhla-Oued Eddahab ME 20.207
L'Oriental MR 13.109 L'oriental N 14.6196

Casablanca-Settat [} 4.76% Lasyoune-Sakis El Hamra N 13.740
Rabat-Salé-Kénitra ' 4,76% Souss-Massa ' 4,56%
Tanger-Tetouan-AI S P

Hoceima ' 3,57% Casablanca-Settat l 3,61%

Souss-Massa [} 230% Gucimim-Oued Noun [} 2,88%

Guelmim-Oued Noun | 119% Rabat-sals-Kéntra | 0,67%
E
Investissement projeté Emplois

Dakhl-Oued Ecclatatr E 31.0406 L'oriental EN 5.0 505
L'oricntal IN 20.3206 Delchla-Oued Eddahat E 27.7555
Casablanca-Scttat E 16,80% Laäyoune Sakio El Harre I 16.2206
Laäyoune-Sakia El Hamra E 11.209 Casablanca-Settat M 10.22%

T3“9ÊZÊÊËÎ“'A‘ I 2>> Rabat-Salé-Kénitra J 6.54%
Souss-Massa J 5.69% Tanger-Tetouan-Al Hoceima [ 4.05%
Rabat-Salé-Kénitra [} 1.97% Souss-Massa [} 3.08%
Guelmim-Oued Noun | 165% Guelmim-Oued Noun | 108%
P.

L É



3.8 Secteur de l’Enseignement et de la Formation

16 projets d’investissement dans le secteur de l’Enseignement et de la Formation ont
bénéficié, au cours de l’année 2023, de la mobilisation, par l’Etat (Domaine Privé),
d’une superficie globale de plus de 13 Ha.

Ces investissements d'une enveloppe globale de 169 Mdh, devraient générer la
création, à terme, de 551 emplois escomptés.

De plus, 84% de la superficie mobilisée au profit de ce secteur concerne la région de
Dakhla-Oued Eddahab.

De même cette région a enregistré, à elle seule, plus de la moitié des projets
accordés, du montant global investi et des postes d’emploi à créer au profit de ce

secteur, au cours de l’année 2023.

Nbre Projets Superficie mobilisée

Dakhla-Oued Eddahab — 83.59%

Casablanca-Settat l 8,75%

Dakhla-Oued Eddahab

Laäyoune-Sakia El Hamra

Laäyoune-Sakia El

L'Oriental P r l 5,53%

Tanger-Tetouan-AI
Hoceima

Tanger-Tetouan-AI

Hoceima l 142%

Casablanca-Settat

L'Oriental ‘ 0,71%

Investissement projeté Emplois

pattis-Ouec Ecconse NNN 5 | | 02620006 scc E 52005
Laäyoune-Sakia El sTm
Laäyoune-Sakia El Hamra - 19,11% Hamra e

Casablanca-Settat - 11,83% Casablanca-Settat l 8.17%
Tanger-Tetouan-AI P | l
Hoceima l 7,10% L'Orienta 7,26%
" Tanger-Tetouan-AI
L'Oriental l 4,61% Hoceima l 6,71%

yN



3.9 Secteur du Sport

R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

Au titre de l’'année 2023, l’Etat (Domaine Privé) a mobilisé une superficie de 9,4 Ha,

au profit de 9 projets dans le secteur du Sport, pour un investissement global de

70 Mdh correspondant à la création, à terme, de 498 postes d’emploi.

Au cours de cette période, c’est la région de Casablanca-Settat qui a capté plus de

65% de la superficie mobilisée au profit de ce secteur.

Cette région a bénéficié d’environ 11%

des projets accordés,

global investi et de 80% des postes à créer, en faveur de ce secteur.

de 57% du montant

Nbre Projets

L'Oriental

Dakhla-Oued Eddahab

Laävoune-Sakia El Hamra

33,5%

Superficie mobilisée

Casablanca-Settat

L'Oriental

Dakhla-Oued Eddahab

N =-

Casablanca-Settat - 1196 Béni Mellal-Khénifra l 2,9%
Béni Mellal-Khénifra - % Laäy°:gîêjk'a Ël 02%
Investissement projeté Emplois

Casablanca-Settat

L'Oriental

Dakhla-Oued Eddahab

Laäyoune-Sakia El Hamra

Béni Mellal-Khénifra

|

|

Casablanca-Settat

Dakhla-Oued Eddahab

L'Oriental

Laäyoune-Sakia El
Hamra

Béni Mellal-Khénifra



3.10 Secteur de la Santé

L’Etat (Domaine Privé) a accompagné les investissements dans le secteur de la
Santé, par la mobilisation, au cours de l’année 2023, d'une superficie de 1668 Ha, en
vue de réaliser 7 projets d’'investissement, pour une enveloppe globale de 914 Mdh

correspondant à la création, à terme, de 1.046 emplois escomptés.

Presque la moitié de la superficie mobilisée au profit de ce secteur a été enregistrée

au niveau de la région de Tanger-Tétouan -Al Hoceima.

Au titre de l’année 2023, cette région a bénéficié de plus de 14% des projets
accordés, de plus de la moitié du montant global investi et des postes à créer, en

aveur de ce secteur.

Nbre Projets Superficie mobilisée
T: -T -AI
Tanger-Tetouan-AI ; _
e rétou E 1.20 Deraa-Tafialet JRN 22.7356
Laâäyoune-Sakia El Hamra - 14,29% L'Oriental - 17,82%
Deraa-Tafilalet NNN 14.207 Dakhla-Oued Eddahab ' 8,33%
Dakhla-Oued Ecdatab JIN 14.2055 Laäyoune-Sakia El Harnra | 2,37%
; e S #
Investissement projeté Emplois

Hoceima Hoteima 57,36%
L'Oriental - 26,25% L'Oriental - 27,25%

Deraa-Tafilalet MRE 10.725 Deraa-Tafilalet [} 8,03%
Dakhla-Oued Eddahab [} 8.20% Dakhla-Oued Eddahab | 6.50%
Laäyoune-Sakia El Hamra | 0,14% Laëyoune-Saka El | 0,67%
mra

3.11 Autres secteurs d’activité
L’Etat (Domaine Privé) a mobilisé, au cours de l’année 2023, une superficie globale
de plus de 468 Ha, dédiée à la réalisation des équipements au niveau de la région de

Laâyoune-Sakia El Hamra (la ceinture verte Nord, la ceinture verte Sud, extension de

a décharge Communale etc…), pour un investissement global de 345 Mdh

permettant la création de 68 postes d’emploi.

VN



E POUR L’INVESTISSEMENT

R LE FONCIER PUBLIC MOB

4. Ventilation par Région
> La ventilation des projets approuvés par région, au titre de l’année 2023, place

les projets de la région de Dakhla-Oued Eddahab en 1°' position avec plus de

53%, suivie par la région de Laäyoune-Sakia qui arrive en 2°"° position avec

plus de 21% du total des projets agrées.

Dakhla-Oued Eddahab
Laäyoune-Sakia El Hamra
L'Oriental
Tanger-Tetouan-Al Hoceima
Guelmim-Oued Noun
Casablanca-Settat
Rabat-Salé-Kénitra
Souss-Massa
Marrakech-Safi

Béni Mellal-Khénifra
Fès-Meknès
Deraa-Tafilalet

Nbre projets

—— 55.22>
P 21.22
E 0255
E 6.22%
H 322
H 258%
H 172%
H 107%
l 0,64%
| 0.44%
| 0.21%
| 0,21%
#

> La répartition régionale du foncier mobilisé, fait ressortir, qu’au cours de cett

période, la régio

n de Dakhla-Oued Eddahab s'accapare près de 83% de

superficie globale mobilisée.

Dakhla-Oued Eddahab
Laäyoune-Sakia El Hamra
Tanger-Tetouan-Al Hoceima
Guelmim-Oued Noun
Rabat-Salé-Kénitra
Casablanca-Settat
L'Oriental

Autres

Marrakech-Safi

Superficie mobilisée

E 137>
E 215x

| 0.54%
| 0.28%
| 0,22%
| 0.20%
0.06%

0,05%

e

a


> En termes des investissements projetés, ce sont les régions de Laâyoune-Sakia
El Hamra, de Tanger-Tétouan-AIl Hoceima et de Dakhla-Oued Eddahab qui ont

bénéficié de 93% du montant global investi.

Investissement projeté

Laäyoune-Sakia El Hamra E 52.110
Tariger-Telouan-Al Hoceirna E 21.617
Dakhla-Oued Eddahalo N 13,25%

L'Oriental M 230%
Casablanca-Settat [} 174%
Guelmim-Oued Noun F 1.14%
Rabat-Salé-Kénitra [ 0.86%
Souss-Massa | 0,36%
Marrakech-Safi | 0.26%
Deraa-Tafilalet | C.26%

Béni Mellal-Khénifra  0,06%
Fès-Meknès . 0,05%

> Encore plus, près de 80% des postes d’emploi à créer, sont concentrés au
niveau de quatre régions: Dakhla-Oued  Eddahab, Tanger -Tétouan -AI

Hoceima, Laâäyoune -Sakia El Hamra et Rabat-Salé- Kénitra.

Emplois

Dakhla-Oued Eddahab E 50.652
Tanger-Tetouan-Al Hoceima E 22 5 70
Laäyoune-Sakia El Hamra DE 13.532
Rabat-Salé-Kénitrs E 12.050
L'Oriental E 0. 7506
Casablanca-Settat NNN 5.45%
Guelmim-Oued Noun I 2,61%
Souss-Massa M 103%
Marrakech-Safi } 0.61%
Deraa-Tafilalet J 0,41%
Béni Mellal-Khénifra | 0.27%
Fès-Meknès | 0,15%

yN


RAPPORT SUR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

4.1 Dakhla-Oued Eddahab : Mobilisation du foncier en appui aux secteurs de l’Energie
et des Mines

La région de Dakhla-Oued Eddahab a enregistré la mobilisation de 11120 Ha (soit
83% de la superficie globale mobilisée au cours de l’année 2023), destinés à recevoir
248 projets d'investissement, pour une enveloppe globale de 5.048 Mdh et devant

générer la création, à terme, de 6.281 postes d’emploi.

Ces projets d'investissement concernent principalement les secteurs de l'Energie et
des Mines avec un pourcentage de 92% de la superficie mobilisée au niveau de cette
région.

En termes de nombre de projets approuvés, au cours de cette période, le secteur du
Tourisme a bénéficié de plus de 32% des projets accordés au niveau de cette région

suivi, respectivement, par le secteur de l'Industrie (environ 23%), le secteur des
Services (16%) et le secteur de l’Agro-Industrie (9%).
Nbre Projets Superficie mobilisée
Tourisme EN 32.269 Encrsic NN 62,99%
Industrie EN 22,58% Mines N 28,97%
Servicos IMMN 16,13% Habitat J 5,55%
- 9
Agro-industrie IMN 9,27% Industrie | 1,77%
Habitat I 8,47%
Agro-industrie | 1,40%
Mines M 6,05%
Enseignement et Formation . 3,23% Tourisme l 126%
Sport } 1.21% Services  0,12%
Energie J 0,40% Enscignement et Formation | 0,10%
Santé | 0,40% Sport  O,01%
\ #X #
Investissement projeté Emplois
Habitat E 553506 Tourisme EN 50.57%
Tcurisme EN  21,41% Industrie M 15.73%
Industrie IMN 16.780 Agro-industrie B 9.27%
Agro-industrie NNN 17.77% services BI 8.18%
sa %
rvices I 3,79% Energie B} 5,41%
Energie } 3,24%
Enseignement et Formation _ 4,57%
Mines M 3,06%
9
Enseignement et Formation B 1,92% lUnes ' Ss
santé } 149% Santé | 1m%
Sport | 0.20 Sport | 0,88%

L É


4.2 Lagyoune-Sakia El Hamra : Mobilisation du foncier en appui au secteur des Mines

Au titre de l’année 2023, la région de Laâyoune-Sakia El Hamra a bénéficié de
l’approbation de 99 projets d'investissement, à réaliser sur des assiettes foncières
d’une superficie globale de l’ordre de 1845 Ha, soit 14% de la superficie globale
mobilisée.

Ces projets d’investissement d'une valeur de plus de 21960 Mdh devraient générer, à

terme, la création de 2771 postes d’emploi.

Au cours de cette période, c’est le secteur des Mines qui a centralisé plus de 41% de

la superficie globale mobilisée au niveau de cette région.
Au cours de cette période, les secteurs des Services, de l’Habitat et des Mines ont
bénéficié d’environ 55% des projets approuvés au titre de l'année 2023.
re rrojets ici ilisé
j ( Superficie mobilisée
E 10.10>
Mines EN 171706 d'activité P
Agro-industris MMN 16,16% Haoitet e 24.06%
industrie NNN 11,110 Industrie MI 5,99%
Tourisme I 8,07% Tourisms | 0,88%
Enseignement et Formation | 4.04% Agro-industric | 0,83%
Autres secteurs d'activité B 4,04%
Services | 0,50%
Santé J 102% E ut
nseignement e
Sport J 102% Formation 0.05%
Investissement projeté Emplois
ex Agro-industrie — 35,47%
ines EN 70
Heoieet B 8446 industrie I 19.529
Industrie Ÿ 3,03% Mines R 15.75
Agro-industrie | 1,97% Services M 10,83%
Tourisme | 0,67% Tourisme } 7.76%
Services | 0,40% Enseignement et Formation [} 5.12%
Autres secteurs d'activité | 0,16% Autres secteurs d'activité Ÿ 2,45%
Enseignement et Formation | 0,15% Santé | 0.25%
Santé 0,01% Sport | 0,23%

yN



RAPPORT SUR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

4.3 Tanger-Tétouan-AI Hoceima : Mobilisation du foncier en faveur des secteurs de
l’Energie et de l’Industrie

La région de Tanger-Tétouan-AI Hoceima a enregistré, au cours de l’année 2023, la
mobilisation d’une superficie globale de 289 Ha, destinée à recevoir 29 projets
d'investissement pour une valeur totale de plus de 8165 Mdh correspondant à la

création, à terme, de 4.621 postes d’emploi.

Au cours de cette période, les secteurs de l’Energie et de l’Industrie ont profité de

84% de la superficie mobilisée au niveau de cette région.

En termes de nombre de projets approuvés, le secteur de l'Industrie a bénéficié de
près de 38% des projets accordés au niveau de cette région, suivi, respectivement,
par le secteur du Tourisme (31%), le secteur des Services (10%) et le secteur de
‘Energie (7%).

Nbre Projets Superficie mobilisée

Services - 10,34% Services ' 9,63%

Energie - 6,90% Tourisme l 3,79%
Habitat [} 3,45% Habitat | 1,32%
santé } 3.45% Santé _ 0.28%
Agro-industrie [} 3,45% Agro-industrie | 0,23%
Enseignement et 0 Enseignement et

Formation ' 545% Férmation 0,07%

Investissement projeté Emplois

Energie NNN 60.6256 vrccustri - N 55 106
industrie EN 23.59% Tourisme M 15.19%

Tourime } 7,88%
Santé - 6.12%
Habitet | 0,64%

Santé M 12.98%
Agro industrie } 280%

s 9
Services | 0,63% ervices | 16%
Agro-industrie | 0,37% Energie | 1.30%

Enseignement et Formation | 0,15% Enseignement et Formation | 0,82%

L É



4.4 Guelmim-Oued Noun : Mobilisation du foncier en faveur des secteurs de
l'Agro-Industrie et des Mines

15 projets d'investissement, à réaliser sur une superficie globale d’environ 73 Ha, ont
été approuvés au niveau de la région de Guelmim-Oued Noun, pour une enveloppe
globale de plus de 432 Mdh et devant générer la création, à terme, de 534 postes

d’emploi.

85% de la superficie mobilisée au niveau de cette région, est destinée à recevoir des

projets d’investissement dans les secteurs de l'Agro-Industrie et des Mines.

Au cours de cette période, le secteur du Tourisme a bénéficié, de plus de 53% des
projets accordés au niveau de la région, suivi, respectivement, par le secteur des
Mines (20%), le secteur de l’Agro-Industrie (13%) et les secteurs de l‘Industrie et des
Services (presque 7% chacun).

Nbre Projets Superficie mobilisée

Tourisme

Agro-industrie

Mines - 20,00% Mines
Agro-industrie - 13,33% Tourisme

Industrie ' 6,67% Industrie
Services ' 6,67% Services
J
Investissement projeté Emplois

Tourisme — 44,20% Tourisme — 38,76%
Agro-industrie — 29,60% Acro-industrie — 34,83%
incustrie N 15.750 mines N 12.75
Mines ' 5,09% ladustrie - 10,49%

Services l 2,36% Services ' 3,75%

pN



E POUR L’INVESTISSEMENT

4.5 Rabat-Salé-Kénitra : Mobilisation du foncier en faveur du secteur de l’Industrie

Au titre de l’année 2023, la région de Rabat-Salé-Kénitra a enregistré la mobilisation

d’une superficie globale d’environ 38 Ha,
d'investissement, principalement dans le

superficie mobilisée au niveau de cette

secteur

région),

dédiée à la
de

réalisation de 8 projets

l'Industrie (soit 98% de la

pour une enveloppe globale de

325 Mdh correspondant à la création, à terme, de 2.651 postes d’emploi.

Pendant cette période,
de
‘Industrie (environ 38%) et

e secteur des

accordés au niveau cette région,

Services a bénéficié de 50%

suivi,

des projets

respectivement, par le secteur de

le secteur du Tourisme (presque 13%).

Nbre Projets

Services 50%

Industrie 37,50%

Tourisme 12,50%

Superficie mobilisée

Services l 123%

Tourisme ‘ 0,56%

Investissement projeté

Industrie 96,26%

Services | 3,74%

Emplois
(péverrs - 95'44%

Services l 4,56%

L É



4.6 Casablanca-Settat : Mobilisation du foncier en faveur des secteurs de l’Industrie,
du Tourisme et du Sport

12 projets d'investissement, à réaliser sur une superficie globale d'environ 30 Ha, ont
été approuvés au niveau de la région de Casablanca-Settat, pour une enveloppe
globale de l’ordre de 657 Mdh devraient générer la création, à terme, de 1.116 postes

d’emploi.

Les secteurs de l’Industrie, du Tourisme et du Sport, sont les principaux bénéficiaires
de cette mobilisation à travers 85% de la superficie mobilisée au niveau de cette
région.

Nbre Projets Superficie mobilisée

sr vices N =1 ircuistrie N 07155
Industrie - 16,67% Tourisme - 23,77%
Tourisme - 16,67% Sport - 20,48%

Sport - 8,33% Services - 8,39%

Ÿ Ÿ Enseignement et *

Agro-industrie - 8,55% Formation l 4,00%

Enssignerent e MR 9359 Agro-industrie [} 240%
Hebitat NNN 8330 Habitat | 0,25%
Investissement projeté Emplois

Tourisme - 18,49%
services I 15.76%

Sport J 500x
Tourisme 16,31%

Agro-industrie ' 3,80%

Enseignement et | Z Agro-industrie ' 4,48%
Formation a086

; Enseignement et °

Habitat l 2,59% Formation A,03%

d



SE POUR L’INVESTISSEMENT

4.7 L’Oriental : Mobilisation du foncier en appui aux secteurs des Services, de
l’Agro-Industrie et de l’Industrie

Au cours de l’année 2023, l'Etat (Domaine Privé) a mobilisé, au niveau de la région
de l’Oriental, une superficie globale de plus de 26,5 Ha, destinée à recevoir

43 projets d’investissement.

Plus de 87% de la superficie mobilisée au niveau de cette région, est destinée à
recevoir des projets d'investissement  dans les secteurs des Services,  de

’Agro-Industrie et de l’Industrie.

Ces investissements d’une valeur globale de plus de 868 Mdh correspondant à

v

création, à terme, de 1.997 postes d'emploi couvrant, principalement, les secteurs de
la Santé, de l’Industrie et de l’Agro-industrie.

Nbre Projets Superficie mobilisée

5,58% Services 38,20%

23,26% Agro-industrie — 31,66%

Services

Agro-industrie

industrie NNN 16.2606 industrie NNN 17.205.

Tourisme NNN 16.2206 Sport B} 651
Sport - 6.98% Tourisme ' 4,84%
santé E 56.005 santé | 113%

Enseignement et -
4,64% Enseignement et
Formation Formation ‘ 0.,37%

Investissement projeté Emplois

Industrie — 24,66% Industrie — 22,7%

Agro-industrie

19,68% Agro-industrie NNN 16,27%

Services

14,43% Tourisrne NNN 14.5206
Tourisme MR 10.61> sonté NNN 1+.27%
- Enseignement et ,
Sport [} 207% ETEN E R 200%
Enseignement el
Formation l 0.90% Sport l fs

L É


4.8 Marrakech-Safi : Mobilisation du foncier en faveur du secteur de l’Industrie

La région de Marrakech-Safi a concentré, au titre de l’année 2023, la mobilisation

d’une superficie d'environ 7 Ha, destinée à recevoir 3 projets d'investissement, pour

un capital global de plus de 99,7 Mdh correspondant à la création, à terme, de

124 emplois escomptés.

Le secteur de l'Industrie est le principal bénéficiaire de cette mobilisation à travers

60% de la superficie mobilisée au niveau de cette région.

En termes des investissements à réaliser, au cours de cette période, le secteur du

Tourisme a bénéficié de 70% du montant globa

investi au niveau de cette région.

Nbre de Projet Superficie mobilisée
és — S (névatrie — 6076
en - L Tourisme - (O
Investissement projeté Emplois
Tourisme — _ Tourse —Se%
(nausrie - e (naustre — s66

d



E POUR L’INVESTISSEMENT

4.9 Souss -Massa : Mobilisation du foncier en appui aux secteurs des Services et de
l’Industrie

Au cours de l’année 2023, la région de Souss-Massa a enregistré la mobilisation
d’une superficie globale de 65 Ha, destinée à recevoir 5 projets d’'investissement,
pour une enveloppe globale de 135 Mdh permettant la création, à terme, de

210 postes d’emploi.

89% de la superficie mobilisée au niveau de cette région, est destinée à recevoir des

projets d’investissement dans les secteurs des Services et de l'Industrie.

De même pour les investissements à réaliser et les postes d’emploi à créer, les deux
secteurs précités ont enregistré, respectivement, 74% du montant global investi et

73% des postes à créer au niveau de cette région.

Nbre Projets Superficie mobilisée

Tourisme — 40% Services — 49%
Services — 40% Industrie - 40%
Industrie - 20% Tourisme - 119

Investissement projeté Emplois
Industrie - 39% Industrie —
Tourisme - 35% Tourisme — 35%
Services - 26% Services - 27%

L É


i PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 ‘

4.10 Fès- Meknès : Mobilisation du foncier en appui au secteur du Tourisme

Au titre de l’année 2023, la région de Fès-Meknès a capté un seul projet dans le

secteur du Tourisme, consistant en
sur une assiette foncière  d’une

l’aménagement d’un parc d'attraction à Meknès,
superficie de 237 Ha, devant drainer un

investissement de 20 Mdh et générer la création, à terme, de 30 postes d’emploi.

4.11 Deréa-Tafllalet : Mobllisation du foncier en appul au secteur de la Santé

Cette région a pu accrocher un seul projet d'investissement dans le secteur de la

Santé, sur un foncier domanial, d’une superficie de 3824 m’, devant drainer un

investissement de 98 Mdh et générer la création, à terme, de 84 postes d’emploi.

4.12 Béni Mellal-Khénifra : Mobilisation du foncier en appui au secteur du Sport

Cette région a pu accrocher 2 projets d'investissement, sur un foncier domanial,

d’une superficie globale de 3.684 m°, devant drainer un investissement de 21,7 Mdh

et générer la création, à terme, de 55 postes d’emploi.

75% de la superficie mobilisée au niveau de cette région, est destinée à recevoir un

projet d’investissement dans le secteur du Sport.

Nbre Projets

Tourisme

Sport

Superficie mobilisée

s076 Sport —75%
50% Tourisme - 25%

Investissement projeté

ds - 06

Sport l 4%

Emplois

Tovrsme — P
Sporl l 9%

yN



RAPPORT SUR LE FONCIER PUBLIC MOBI E POUR L’INVESTISSEMENT

Il. MOBILISATION DU FONCIER DANS LE CADRE DU PARTENARIAT
AGRICOLE - ANNEE 2023 -

Le partenariat public-privé pour la mise en valeur des terrains agricoles consiste en
la location de longue durée (17 à 40 ans selon le type de projet) de terrains au profit
de promoteurs qui s’engagent, dans un cadre contractuel avec l’Etat, à entreprendre
des projets d’investissement permettant une bonne valorisation de ce foncier tout en
créant de l'emploi en milieu rural.

Ces terrains sont attribués dans le cadre d'appels d'offres lancés au niveau central
par l’Agence pour le Développement Agricole et pilotés par une Commission
Interministérielle Technique composée également de la Direction des Domaines de
l’Etat, la Direction des Affaires Rurales relevant du Ministère de l'Intérieur ainsi que
l'Agence  Marocaine de Développement des Investissements et des Exportations
relevant du Ministère de l’Industrie et du Commerce.

En vue d’encourager la participation des petits agriculteurs dans l’opération du
partenariat public-privé, des appels d'offres régionaux sont également lancés, dédiés
aux petites parcelles ayant une superficie inférieure à 5 ha en irrigué et à 10 ha en
bour, selon une approche décentralisée avec un pilotage assuré par des
Commissions Régionales Techniques instituées à cet cffet. Cette opération donne la
possibilité aux petits agriculteurs exploitant ces terrains de les louer pour une longue
durée de 17 ans renouvelable au lieu de la location pour une seule année sur la base
des enchères publiques. Elle leur permet ainsi l’engagement des investissements
pérennes et la possibilité de bénéficier des subventions de l’Etat dans le cadre du
Fonds de Développement Agricole.

L’attribpution des terres agricoles, dans ce cadre, est opérée conformément aux
dispositions de la circulaire N°2/2007 du 29 Janvier 2007 du Premier Ministre
relative aux modalités de location des terres agricoles relevant du domaine privé de
l’Etat, ainsi que du règlement de l’appel d'’offres élaboré par la commission
interministérielle chargée du partenariat public privé autour des terres agricoles du
Domaine Privé de l’Etat.

d



1. Données globales
Au titre de l'année 2023, 179 conventions ont été signées dans le cadre du
partenariat agricole, suite aux appels d'offres organisés à cet effet, portant sur une

superficie de 3.841 Ha, un investissement global de l’ordre de 685 Mdh et permettant

la création, à terme, de 1.372 postes d’emploi.

Fès-Meknès 49 2.256ha27a03ca 195 359727 341
derssais n 5 528ha08a54ca _ 146.578.540 175
Hoceima
Casablanca-Settat 10 437ha04a77ca 139.172.551 290
Rabat-Salé-Kénitra 37 248ha73a04ca 124.286.089 267
Béni Mellal-Khénifra 26 139ha13a04ca 24.579.767 83
Souss-Massa 27 126hal7a84ca 12575 322 72
L'Oriental 22 89ha87a08ca 41.153.828 127
laâyoune -Sakia el Hamra 3 15ha68a47ca 4.095.000 1

Total général - Oha 99a 81ca

2. Ventilation par filière

Au titre de l’année 2023, les filières de l'Arboriculture fruitière, de la production
Céréalière et de l’Oléiculture ont bénéficié de la mobilisation d’une superficie globale
d’environ 3.572 Ha, soit environ 93% de la superficie globale octroyée, par l'Etat

(Domaine Privé), au profit des projets d’'Investissement dans le cadre du Partenariat
Agricole.



IR LE FONCIER PUBLIC MOI

Nbre projets

2,23%

168%

9
0568 3,35%

/ 4,47%

-—

31,84%

« Plantes aromatiques et médicinales
» Filière céréalière
» Héliciculture
Apiculture
Agrumiculture
= Filière viandes rouges
Viticulture
Arboriculture fruitière
= Oléiculture

Superficie louée

O-s
0.18% 110%1,82% _3,06%
0.1 |

13,33%

20,86%

» Héliciculture
= Plantes aromatiques et médicinales
= Apiculture
Filière viandes rouges
Vilicullure
= Agrumiculture
Oléiculture
Filière céréalière
= Arboriculture fruitière

0,30%

Investissement projeté
179% _2,56%

A | / 2020

Ts N
p
’ 4,97%
|
12,29%
24,79%

» Plantes aromatiques et médicinales
» Héliciculture
» Filière céréalière

0,44%

Apiculture
Filière viandes rouges
= Agrumiculture
Viticulture
Oléiculture
= Arboriculture fruitière

esx Emplois

4‘1% 4,08%
’ 4,37%

6,56%

7,00%

22,38%

« Plantes aromatiques et médicinales
= Héliciculture
» Filière céréalière
Apiculture
Filière viandes rouges
= Agrumiculture
Viticulture
Oléiculture
= Arboriculture fruitière

SE POUR L’INVESTISSEMENT



2.1 Arboriculture fruitière

Au cours de l’année 2023, l'Etat (Domaine Privé) a loué une superficie globale
d'environ 2.259 Ha au profit de 57 projets, spécialement, dans la filière de
l’Arboriculture fruitière, soit environ 59% de la superficie globale mobilisée au profit
des projets d’Investissement dans le cadre du Partenariat Agricole.

Ces projets devraient drainer un investissement global de l’ordre de 335 Mdh et
générer la création de 721 postes d'emploi.

De plus, avec une superficie globale de 1.275 Ha, la région de Fès-Meknès bénéficiera
de la réalisation de 16 projets dans la filière de l’Arboriculture fruitière pour une
enveloppe globale de l’ordre de 98 Mdh permettant la création de 249 postes
d'emploi.

Nbre projets Superficie louée
Rabat-salé-kénitra E =1.55. Fès-Meknès PE
Fès-Meknès EN 28.07% Tanger Tétouan A!…. NNN 23.229
Béni Mellal-Khénifra MEN 10.55% Casablanca-Settat I 7.83%
L'oriental MEN 10.5306 Rabat-salé-kénitra [} 4.82%
Casablanca-Settat M 8.77% Béni Mellal-Khénifra [}} 3.74%
Tanger Tétouan AI... MM 7.02% Souss-Massa [} 287%
Souss-Massa } 3.51x L'oriental | 1.07%
Investissement projeté Emplois
Tanger Tétouan Al Hoceima Fès-Meknès _
cès-Meknès NNN 20.2555 Tanger Tétouen Àl In
Casablanca-settat NN 12,41%6 Casablanca-Settat — 22,33%
Rabat salé kénitra - 11,65% Rabat-salé-kénitra - 11,10%
Béni Mellat-Khénifra | 166% Béni Mellal-Khénifra } 4.02%
L'oriental l 1,25% L'eriental - 4,02%
Souss-Massa | 0,87% Souss-Massa | 0,42%
À

yN



2.2 Filière Céréalière

L'Etat (Domaine Privé) a loué 801 Ha au profit de 3 projets dans la filière Céréalière,
soit près de 21% de la ssuperficie globale mobilisée au profit des projets

d’Investissement dans le cadre du Partenariat Agricole au titre de l’année 2023.

Ces projets devraient drainer un investissement total d’environ 12 Mdh et générer la

création, à terme, de 33 postes d’emploi.

Avec une superficie globale de 793 Ha, la région de Fès-Meknès bénéficiera de la
réalisation d’un seul projet dans la filière céréalière pour une enveloppe globale de
’ordre de 10 Mdh permettant la création de 25 postes d’emploi.

Nbre projets Superficie louée
L'oriental — 33,33% L'oriental l 0,74%
s
Investissement projeté Emplois
L'oriental ' 12.16% Souss-Massa - 12,12%
Souss-Massa | 109% L'oriental - 12,12%

L É


2.3 Oléiculture

La filière de l’Oléiculture a capté une superficie totale de 512 Ha, au profit de 66
projets, soit 13 % de la superficie mobilisée dans le cadre du Partenariat Agricole,
pour une enveloppe globale de l’ordre de 169 Mdh permettant la création de 307

postes d’emploi.

De plus, les régions de Fès-Meknès et de Casablanca ont enregistré, au cours de

cette période, 76% de la superficie mobilisée au profit de cette filière.

Nbre projets Superficie louée

Souss-Massa Casablanca-Settat _
ri Meal-<hérifre | 2 2055 Fès-Meknès NN 25.4606

Fès-Meknès - 18,18% Béni Mellal-Khénifra - 9,69%
Rabat-salé-kénitra - 10,61% Souss-Massa ' 5,73%

Casablanca-Settat J 7585 Rabat-saié-kénitre }} 5.20%
L'oriental l 3,.03% L'oriental l 2,41%
Tanger -Tétouan-Al l Tanger -Tétouan-AI
Hoceima Ll Hoceima | 0.65%
Investissement projeté Emplois

csablance-settot E s7565 | | ca<acionca-cottot e 2 025
Fès-Meknès E 17.06x Béni Mellal-khénifra N 14,66%
Béni Mellal-Khénifra ' 9,56% Souss-Massa - 13,68%

Rabat-salé-kénitra ' 7,75% Rabat-salé-kénitra - 10,10%
Souss-Massa l 316% Fès-Meknès - 9,77%
L'oriental l 2,43% L'criental - 8,14%

Tanger -Tétouan-AI Tanger Tétouan AI
Hoceima 155% Hoceima

A



E POUR L’INVESTISSEMENT

2.4 Agrumiculture

L'Etat (Domaine Privé) a mobilisé 1355 Ha au profit de 8 projets dans la filière de
l’Agrumiculture, soit près de 3% de la superficie globale mobilisée au titre de l'année
2023, pour une enveloppe globale de l’ordre de 34 Mdh permettant la création de 90

postes d'emploi.

De plus, les régions de Rabat-Salé-Kénitra, de l’Oriental et de Souss -Massa ont
bénéficié de la quasi-totalité de la superficie mobilisée au profit de cette filière

avec plus de 97%, au cours de cette période.

Nbre projets Superficie louée °
Rabat-salé-kénitra ' 12,50% L'oriental - 29,83%
Souss-Massa ' 12,50% Souss-Massa - 26,22%
Béni Mellal-Khénifra ' 12,50% Béni Mellal-Khénifra l 2,64%
Investissement projeté Emplois
L'érientäl Rabat-salé-kénitra - 38,89%
Rabat-salé-kénitra - 32,14% L'oriental - 34,44%
Souss-Massa ' 1164% Souss-Massa - 25,56%
Béni Mellal-Khénifra l 4,25% Béni Mellal-Khénifra } 1.11%
d

L É


i PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 \
Z. Déclinaison Régionale

> La ventilation régionale des conventions établies fait ressortir que 48% des
projets approuvés, sont concentrés au niveau de deux régions : Fès -Meknès et

Rabat -Salé -Kénitra.

> Environ 84% de la superficie globale mobilisée, est enregistrée au profit de

trois régions : Fès-Meknès, Tanger-Tétouan-AI Hoceima et Casablanca-Settat.

Nb projets Superficie louée

Fès-Meknès

Rabat-salé-kénitra

Souss-Massa

Béni Mellal-Khénifra

E 2067
H 15.08>
E 1-5=

Fès-Meknès

Tanger Tétouan AI
Hoceima

Casablanca-Settat

Rabat-salé-kénitra

Fès-Meknès

Tanger Tétouan AI
Hoceima

Casablanca-Settat
Rabat-salé-kénitra
L'Oriental

Béni Mellal-Khénifra

Souss-Massa

Laäyoune -Sakia el
Hamra

E 2130
E 2050
l RS
E 500>

|

J 180x

0,60%
|

L'orental MRN 12.20x Béni Mellal-Khénifra [} 3.62%
Casablanca-Settat ' 5,59% Souss-Massa l 3,29%
Tangâr{3‘£î\tät;äﬁ AI l 2,79% L'Oriental I 2,34%
Laayoæ;—fäakia el l 168% Laäyoune -Sakia el Hamra ‘ 0,40%
—
Investissement projeté Emplois

Fès-Meknès
Casablanca-Settat

Rabat-salé kénitra

Tanger Tétouan AI
Hoceima

L'Oriental
Béni Mellal-Khénifra
Souss-Massa

Laäyoune -Sakia el Hamra

|
E =-
E .

| =

yN


R LE FONCIER P!

SE POUR L’INVESTISSEMENT

3.1 Fès-Meknès (Arboriculture fruitière)
Au titre de l’année 2023, la région de Fès-Meknès a bénéficié de la signature de 49

conventions dans le cadre du partenariat agricole, dédiées principalement aux
filières de l’Arboriculture fruitière et la filière Céréalière.

Ces investissements devraient être réalisés sur une superficie globale de plus de
2.256 Ha, soit environ 59% de la superficie mobilisée au titre de l’année 2023, pour

un investissement global de 193 Mdh permettant la création, à terme, de 341 postes
d'emploi.

Nbre projets 0179 SUPerficie louee _1,89%
2,04% * 00 0,37%
oy/ 204% 612% 7%6—031% _— _578%
35,19%
24,49%
24,49%

= Filière céréalière » Hélicicullure » Hélicicuitüre « Apieultüre

Apiculture = Filière vandes rouges Filière viandes rouges » Viticulture

Oléiculture Viticulture Oléiculture Filière céréalière
= Arboriculture fruitière = Arboriculture fruitière

Investissement projeté 0esx — Emplois _176% , 52%
0,/8%_ 3,37% ; .
/ 5,52% — 469%
7,70% TS3
15,75%
16.25%

= Héliciculture = Apiculture = Héliciculture * Apiculture

Filière céréalière Filière viandes rouges = Viticulture Filière viandes rouges

Oléiculture Viticulture Filière céréalière Oléiculture
« Arboriculture fruitière = Arboriculture fruitière



3.2 Tanger-Tétouan- Al Hoceima (Arboriculture fruitière)
Au titre de l’année 2023, la région de Tanger-Tétouan- Al Hoceima a enregistré la
signature de 5 conventions dans le cadre du partenariat agricole, d’une superficie

globale de 528 Ha, un investissement global de plus de 146 Mdh permettant la
création, à terme, de 175 postes emplois.

De plus, c’est la filière de l’Arboriculture fruitière qui s'accapare plus de 99% de la
superficie mobilisée au niveau de cette région. De même, pour les investissements et
les emplois à créer, ces filières concentrent presque la totalité.

Nbre projets Superficie louée

0,63%

Oléiculture « Arboriculture fruitière

Cléiculture = Arboriculture fruitière

Investissement projeté Emplois

1,83% 2,86%

Oléiculture « Arboriculture fruitière Cléiculture « Arboriculture fruitière

VN



RAPPORT SUR LE FONCIER P!

SE POUR L’INVESTISSEMENT

3.3 Casablanca-Settat (Oléiculture)

La région de Casablanca-Settat a bénéficié, au titre de l’année 2023, de 10
conventions signées dans le cadre du partenariat agricole, pour une superficie
globale de plus de 437 Ha, et un investissement global de 139 Mdh, dans les filières
de l’Oléiculture (60%) et de l’Arboriculture fruitière (40%).

Nbre projets Superficie louée
50%
Arboriculture fruitière = Oléiculture Arboriculture fruitière = Oléiculture
E
Investissement projeté Emplois
44,48%
Arboriculture fruitière « Oléiculture = Arboriculture fruitière Oléiculture J

L É


3.4 Rabat-Salé-Kénitra (Arboriculture fruitière et l’Agrumiculture)

Cette région a profité de la signature de 37 conventions conclues dans le cadre du

partenariat agricole, au titre de l’année 2023, d’une superficie globale de plus

de

248 Ha, un investissement global de 124 Mdh et permettant la création, à terme, de

267 postes d'emploi.

De plus, ce sont les filières de l’Arboriculture fruitière, de l’Agrumiculture et de
’Oléiculture qui s'accaparent environ 74% la superficie mobilisée au niveau de
cette région.
270x A bre projets 2a_ Superficie louée
T— 2,70% —2 4,50%
8,11%
On A
10,87%
18,92%
19,55%
» Agrumiculture _ * Plantes aromatiques et médicinales
Plantes aromatiques et médicinales Filière viandes rouges
Apiculture Viticulture
» Filière viandes rouges = Apiculture
Viticulture Oléiculture
Oléiculture Agrumiculture
« Arboriculture fruinère = Arboriculture fruitière
Investissement projeté Emplois
659 0,37% _— _— 4112%
165% ___3,74% e
8,82%
11,61%
10,57%
D0 | 1873%
31,43%
. » Plantes aromatiques et médicinales
» Plantes aromatiques et médicinales Filière viandes rouges
Filière viandes rouges Oléiculture
Agrumiculture = Agrumiculture
= Apiculture Apiculture
Oléiculture Viticulture
Arboriculture fruitière = Arboriculture fruitière

VN



3.5 Béni Mellal-Khénifra (Oléiculture)

R LE FONCIER P!

SE POUR L’INVESTISSEMENT

La région de Béni Mellal-Khénifra a profité de la conclusion de 26 conventions
conclues dans le cadre du partenariat agricole, au titre de l’année 2023, portant sur

une superficie globale de 139 Ha, pour une valeur totale de plus de 24 Mdh.

Ces investissements qui concernent

principalement la Filière de l’Oléiculture,

devraient générer la création, à terme, de 83 postes d’emploi.

Nbre projets
3,84%

7,69%
3,85%

23,08%

= Héliciculture Filière viandes rouges

= Agrumiculture Arboriculture fruitière

= Oléiculture

Superficie louée

142%- 4,12%
5,89%

22,67%

Héliciculture Filière viandes rouges

Agrumiculture Arboriculture fruitière

= Oléiculture

Investissement projeté

0,69% _2,23%
O6B% _ 02576

35,68%

» Héliciculture Filière viandes rouges

= Agrumiculture Oléiculture

= Arboriculture fruitière

Emplois
p 1.20%

5
1.20%
S- / 843%

34,94%

Héliciculture » Agrumiculture

Filière viandes rouges Arboriculture fruitière
= Oléiculture



3.6 Souss-Massa (Arboriculture Fruitière)

La région de Souss-Massa a bénéficié de 27 projets d’investissement dans le cadre
du partenariat agricole, au titre de l’année 2023, portant sur une superficie globale
de 126 Ha pour une valeur totale de plus de 12 Mdh.

Ces — investissements … concernent - principalement les filères  de l’Arboriculture
ruitières (51%), de l’Agrumiculture (24%) et de l’Oléiculture (23%).
Nbre projets Superficie louée
3,70% 3,70% 0,97%
7,41%
23,26%
24,45%
« Filière céréalière Agrumiculture « Filière céréalière Oléiculture
Arboriculture fruitière = Oléiculture Agrumiculture = Arboriculture fruitière
Investissement projeté Emplois
° 4,17%
1080 ° 5,56%
23,55%
3194%
32,07%
« Filière céréalière Arboriculture fruitière = Arboriculture fruitière Filière céréalière
Agrumiculture = Oléiculture Agrumiculture = Oléiculture J

yN



RAPPORT SUR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

3.7 L’Oriental (Agrumiculture et Arboriculture fruitière)
Au cours de l’année 2023, la région de l’Oriental a  profité de 22  projets
d’investissement portant, principalement, sur les filières de l’Agrumiculture et de

’Arboriculture fruitière, à réaliser sur une superficie globale de plus de 89 Ha, pour
une valeur globale de 41 Mdh correspondant à la création de 127 postes d’emploi.
(
_— 2,48% 6 2
Nbre pr01et p Superficie louée
— q
T- 2,46% 192%- 4,39%
6,64%
7,40%
14,94% 13,73%
27,61% 26,86%
» Filière céréalière Héliciculture = Héliciculture Viticulture
Filière viandes rouges = Viticulture Filière céréalière « Filière viandes rouges
Arboriculture fruitière » Oléiculture Oléiculture Arboriculture fruitière
= Agrumicullure = Agrumiculture
/ A
Investissement projeté — sn Emplois —318% __ 3189
-— 365% —7.09%
,7,10%
10,21%
19,69%
2290%
» Héliciculture Filière céréalière # Filière céréalière Héliciculture
Filière viandes rouges = Oléiculture Filière viandes rouges m Viticulture
Arboriculture fruitière Viticulture Oléiculture Arboriculture fruitière
= Agrumicullure = Agrumiculture
3.8 Laäyoune -Sakia el Hamra (filière viandes rouges)
La région de Laâyoune -Sakia el Hamra a bénéficié, au titre de l’année 2023, de

3 projets d'investissement dans la filière viandes rouges, à réaliser sur une superficie
de plus de 15 Ha, d'une valeur globale de 4 Mdh permettant la création de 17 postes

d'emploi.

U É


CHAPITRE Il: MOBILISATION DU DOMAINE PRIVE DE
L’ETAT AU TITRE DU 1°" SEMESTRE 2024

|. MOBILISATION DU FONCIER AU PROFIT DE L’INVESTISSEMENT
(HORS PARTENARIAT AGRICOLE)

1. Données globales

Au titre du premier semestre de l’année 2024, 110 projets ayant pour support un
foncier relevant du Domaine Privé de l'Etat, ont été approuvés, pour une superficie
globale de l’ordre de 16.102 Ha, un investissement projeté de plus de 16.464 Mdh
correspondant à la création, à terme, de 16.694 postes d’emploi.

En outre, la totalité de ces projets d’investissement a été approuvée conformément
au nouveau dispositif législatif et réglementaire relatif à la Gestion Déconcentrée de
l'Investissement, notamment la loi-Cadre n°03.22 formant Charte de l'Investissement

—
Jion
pr

rficie mobil

Laâyoune-Sakia El Hamra 25 15 301ha5/a/8ca 5 092 260 000 1094
Casablanca Settat 7 296ha05a30ca 724 000 000 6230
Dakhla-Oucd Eddahab 27 290ha36a48ca 170 918 000 377
Marrakech-Safi S 65ha89a52ca 740 500 000 335
Guelmim-Oued Noun 5 56hal3a49ca 8090 324 803 1086
L'Oriental 15 55ha7la34ca 519 220 525 1316
Tanger-Tétouan-AI Hoceima 9 16ha03a44ca 563 535 499 3930
Rabat-Salé-Kénitra > 14ha38a59ca 187 900 000 1820
Fès-Meknès 5 04ha53a73ca 67 980 000 150
Béni Mellal-Khénifra 4 Olha06a54ca 20 310 000 s5
Souss-Massa 4 OOha93a59ca 270 450 000 260
Deraë-Tafilalet 3 OOhal0a70ca 17 000 000 45



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

2.Ventilation par Mode de mobilisation du Foncier

> Plus de 97% du foncier domanial alloué, par l'Etat (Domaine Privé), au titre du

1” semestre de l'année 2024, est mobilisé par voie de location.

Superficie alouée/Mode de mobilisation

Location 97,61%

Cession 2,35%

Location et Cession _ 0,04%

À

> Encore plus, environ 96% de la superficie mobilisée, par voie de location, est destinée à

recevoir des projets dans le secteur de l’Energie.

Superficie mobilisée par voie de location/Secteur d'activité

Mnes [} 249

Agro-industrie l 0,95%

Services l 0.42%

Industrie l 0,39%

Enseignement et Formation ‘ 0.18%
Sport _ 0,05%

Santé 0,C2%

Tourisme . 0,01%

L É



Z. Ventilation par secteur d'activité
Sur le plan sectoriel, la ventilation des dossiers approuvés par nombre de projets fait ressortir
qu’au titre du 1” semestre de l’année 2024 :

> Plus de 64% des projets sont concentrés au niveau de trois secteurs d’activité (Services,

Industrie ct Agro-industrie).

Nb projets/Secteur d'activité

Services 28,18%

Industrie 23,64%

Agro-industrie 12,73%

Tourisme

8,19%
Enseignement et Formation 5,45%
Santé 5,45%

Ssport 5,45%

Mines 5,45%

Habitat 3,64%

Energie - 0,91%

Culture } 091%

> Plus de 93% de la superficie mobilisée est dominée par le secteur de l’Energie.
Superficie mobilisée/Secteur d'activité

Mines [ 244
Industrie l 2,33%

Agro-industrie | 1,03%

Services l 0,45%

Habitat ‘ 0,18%

Enseignemenl el Formalion ‘ 0.18%

Autres ‘ 0,18%

yN



IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

> Plus de 82% des investissements captés par deux secteurs d’activité : Industrie et
Energie.

Investissement projeté/Secteur d'activité

Agro-industrie E 6.37%

Enseignement et Formation J 3170
Mines M 267%
santé f 188%
Tourisme I 1%
Services }} 0.89%
Habitat } 0.66%
Sport | 0.62%

Culture | 0.35%

> Les secteurs de l’Industrie et de l’Agro-industrie sont les principaux pourvoyeurs
d’emplois des projets approuvés, au titre du 1°” semestre de l’année 2024, avec plus de

79% des postes d’emploi à créer.

( ; , k
Emplois/Secteur d'activité
Agro-industrie — 15,23%
Mines MMN 65.460

Enseignement et Formation - 4,9%
Tourisme MRI 3.41
Services - 2,47%
santé } 240%
Sport I 1,01%
Culture | 0.24%

Energie ‘ 0,12%

U É



3.1 Secteur de l’Energie

Au titre du 1°" semestre de l’'année 2024, l’Etat (Domaine Privé) a réservé, une superficie de
l’ordre de 15.009 ha (soit environ 93% de la superficie globale mobilisée pour l'Investissement,
au cours de cette période), dédiée à la réalisation d’un projet dans le secteur de l'Energie,
portant sur la mise en place d’un parc éolien à Boujdour, d’une valeur globale de plus de

4.500 Mdh correspondant à la création de 20 postes d’emploi.

3.2 Secteur des Mines
L’Etat (Domaine Privé) a mobilisé, au cours du 1°" semestre de l’année 2024, 392 Ha au profit de

6 projets d'investissement dans le secteur des Mines.

Ces investissements d’une valeur totale de 439 Mdh, devraient générer la création, à terme, de

1078 postes d'emploi.

Au cours de cette période, la région de Laäyoune-Sakia El Hamra a enregistré plus de la moitié

de la superficie globale accordée à ce secteur.

Compte tenu de la ventilation régionale des projets, c’est la région de Dakhla-Oued Eddahab

oui a bénéficié de la moitié des projets approuvés en faveur de ce secteur.

Nbre projets Superficie mobilisée )
Dakhla-Qued Eddahab — Laäyoune-Sakia El Hamra
Laävoune-Sakia El Hamra - 33,33% Dakhla-Oued Eddathiab - 36,21%
L'Oriental - 16,67% L'Oriental ' 1,87%
e >
Investissement projeté Emplois
Laâäyoune-Sakia El Hamra l 5,19% Dakhla-Oued Eddahab l 4,17%
Dakhla-Oued Eddahab l 5,13% Laäyoune-Sakia El Hamra | 3,06%

yN



RAPPORT SUR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

3.3 Secteur de l’Industrie

Au titre du 1” semestre de l'année 2024, l'Etat (Domaine Privé) a mobilisé 375 Ha au profit du
secteur de l’Industrie, en vue de réaliser 26 projets d’investissement.

Ces projets devraient drainer un investissement global de l’ordre de 9.064 Mdh et générer la
création, à terme, de 10.644 postes d’emploi.

Plus de 73% de la superficie mobilisée au profit de ce secteur, est concentrée au niveau de la
région de Casablanca -Settat.

S'agissant de la répartition régionale des projets, les régions de Dakhla-Oued Eddahab,
Läayoune -Sakia El Hamra, Fès-Meknès et Tanger-Tétouan-AI Hoceima ont enregistré 65% des
projets approuvés en faveur de ce secteur.

En matière du capital investi, la région de Guelmim -Oued Noun s’accapare de la quasi -totalité
des investissements projetés par un projet totalisant 8.000 Mdh, pour la production du

polysilicium (produit de base pour la production des cellules photovoltaïques)

Dakhla-Qued Eddahab

Laäyoune-Sakia El Hamra

Nbre Projets

R 10.25
I 15.50>

Superficie mobilisée

Casablanca-Settat

Guelmim-Oued Noun

HE 1354%

Guelmim-Oued Noun
Casablanca-Settat

Laaäyoune-Sakia El Hamra

Tanger-Tetouan-AI
Hoceima

Fès-Meknès
Dakhla-Oued Eddahab

L'Oriental

H 526%

H 587%
| 130%
| 0.73%

0,35%

0,08%

Casablanca-Settat

Tanger-Tetouan-AI
Hoceima

Guelmim-Oued Noun
Fès-Meknès
Laäyoune-Sakia El Hamra
Dakhla-Oued Eddahab

L'Oriental

Fes-Meknès N 15.5806 Laëyoune-Sakia El Hamra } 10.87%
Tanger-Tetouan-AI Hoceima — 15,38% Fès-Meknès | 1.16%
Casablanca-Settat — 1,54% Tanger-Tetouan-A| Hoceima | 0,73%
Gueimim-Oued Noun NN 11.545 Dakhla-Oued Eddahab | 0,46%
L'oriental IN 1.54x L'Oriental | 0,03%
Investissement projeté Emplois

| 2E

| 1.32%
| v13%
| 0.77%

| 0.57%

L É



3.4 Secteur de l’Agro-industrie

Au cours du 1” semestre de l’année 2024, l’Etat (Domaine Privé) a mobilisé une superficie
globale d’environ 166 Ha, au profit de 14 projets dans le secteur de l’Agro-industrie, pour une
enveloppe totale de l’ordre de 1.048 Mdh correspondant à la création, à terme, de 2.543 postes
d'emploi.

La quasi-totalité de la superficie allouée au profit de ce secteur, soit 84% de la superficie
mobilisée au titre du 1 semestre de l’année 2024, est concentrée au niveau de la région de
Dakhla-Oued Eddahab, et ce, concomitamment avec la stratégie nationale visant le

développement agricole au niveau des provinces du Sud.

Compte tenu du nombre de projets d’investissement approuvés, la région de Dakhla-

Oued Eddahab a enregistré 35,72% des projets accordés au profit de ce secteur.

Nbre Projets Superficie mobilisée
Dakhla-Oued Eddahab 35,72% Dakhla-Oued Eddahab
L'Oriental - 2143% LaésoyneSaga E
amra
Laäyoune-Sakia El Hamra - 21,43% Guelmim- Oued Noun
Rabal-Salé-Kénitrs J 7.14% L'Oriental
Morrakech-sofi BI 714% Rabat-Salé-Kénitra | 120%
Guelmim- Oued Noun J 7140 Marrakech-Safi | 0,57%
Investissement projeté Emplois
Marrakech-safi ETE Rabat-Salé-Kéritre e Es
uA Laäyoune-Sakia El =
Rebat-Salé-Kénitra [} 8,70% rs E 2575>
Dakhla-Oued Eddahab [} 7.27x Dakhla-Oued Eddahab [} 3.97%
Guelmim- Oued Noun | 8.56 L'Oriental [} 395%
Laäyoune-Sakia El Hamra } 4.28% Guelmim- Oued Noun || 236%
L'Oriental [} 3.05% Marrakech-Sefi | 197%

yN


RAPPORT SUR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

3.5 Secteur des Services

Au cours du 1 semestre de l’année 2024, 72 Ha ont été accordés, par l’Etat (Domaine Privé),
au profit de 31 projets d’investissement dans le secteur des Services.

Ces projets d'investissement d’une valeur totale de plus de 146 Mdh devraient générer la
création, à terme, de 412 emplois escomptés.

Ainsi, environ 88 % de la superficie mobilisée, est concentrée au niveau de la région de

Marrakech -Safi.

Nbre Projets Superficie mobilisée
Dakhla-Oued Eddahat = N SPETaE Marrakeech-Safi — n PE
Laâäyoune-Sakia El Hamra —32,23% Laâäyoune-Sakia El Hamra I 5,61%
Béni Mellal-Khénifra MM 9.68% Dakhla-Oued Eddahab } 4,76%
Souss-Massa } 3.23% L'Oriental | 0,70%
Marrakech-Sati [} 3.23% Guelmim-Oued Noun | 0,41%
L'Oriental } 3,23% Souss-Massa | 0,35%
Guelmim-Oued Noun [} 3.23% Fès-Meknès | 0,25%
Fès-Meknès ' 3,23% Béni Mellal-Khénifrsa | 0,18%
Deraa-Tafilalet [} 3,23% Deraa-Tafilalet | 0,08%
Casablanca-Settat [} 3,23% Casablanca-Sottat | 0,07%
PN ;
Investissement projeté Emplois
Laäyoune-Sakia El Hamra E Laäyoune-Sakia El Hamra 41,02:
Dakhla-Oued Eddahab IN 19.440 Dakhla-Oued Eddahab I 23,30%
Béni Mellal-Khénifra ME 12,50% Béni Mellal-Khénifre MM 12.149
Souss-Massa M 8.20% L'Oriental J 6,07%
Guelmim-Oued Noun - 4,85% Casablanca-Settat - 6.07%
Deraa-Tafilalet J 4.10% Souss-Massa [} 3,64%
Casablanca-Settat [} 3.41% Fès-Meknès [ 2,43%
L'Oriental F 239% Deraa-Tafilalet Ÿ 2,43%
Fès-Meknès | 152% Guelmim-Oued Noun } 2.18%
Marrakech-Safi | 0.35% Marrakech-Safi | 0.72%

L É



3.6 Secteur de l’Habitat

L’Etat (Domaine privé) a mobilisé, au cours du 1°" semestre de l’année 2024, une superficie
globale de plus de 29 Ha au profit de 4 projets d’'investissement dans le secteur de l'Habitat, au

niveau de la région de Läayoune -Sakia El Hamra, pour une enveloppe totale d’environ 108 Mdh.

3.7 Secteur de l’Enseignement et de la Formation

Le secteur de l’Enseignement et de la Formation a bénéficié, au titre du 1°" semestre de l’année
2024, de l'approbation de 6 projets d'investissement, ayant pour support un foncier relevant du
Domaine Privé de l’Etat, d’une superficie globale de plus de 28 Ha.

Ces investissements d’une valeur globale de l’ordre de 522 Mdh, devraient générer la création,
à terme, de 820 emplois escomptés.

De plus, 74% de la superficie mobilisée au profit de ce secteur, est concentrée au niveau de la
région de Casablanca-Settat.

Nombre de Projet Superficie mobilisée

Tanger-Tetouan-AI
Hoceima

=7==0 Tanger-Tetouan-AI sR
Rabat-Salé-Kénitra - 16,67% Rabat-Salé-Kénitra
Laäyoune-Sakia El Hamra - 16,67% Leévoune-Sakia El | 0,24%

L

Casablanca-Settat

1,79%

Investissement projeté Emplois

Tanger-Tetouan-AI Tanger-Tetouan-AI
Hoceima Hoceima 21528

Casablanca-Settat Rabat-Salé-Kénitra

20,12%

Rabat-Salé-Kénitra l 3,92% Casablanca-Settat - 15,85%
Laäyoune-Sakia El
Laävoune-Sakia El Hamra | 0.39% Hamra 2,44%

pN



R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

3.8 Secteur du Tourisme

L’Etat (Domaine Privé) a mobilisé, au titre du 1°" semestre de l’année 2024, des assiettes
foncières, d’une superficie globale d’environ 15 Ha, au profit de 9 projets d’investissement dans
le secteur du Tourisme.

Ces investissements d’une valeur totale de 166 Mdh, devraient générer la création, à terme, de
569 postes d'emploi.

De plus, c’est la région de Rabat -Salé -Kénitra qui va abriter, 22% des projets accordés, 70% de
la superficie mobilisée, 43% du montant global investi et 25% des postes d’emploi à créer au
niveau de ce secteur, traduisant, l’effort déployé en vue de renforcer l’offre touristique au niveau
de cette région.

Nbre Projets Superficie mobilisée

Dakhla-Oued Eddahab

Rabat-Salé-Kénitra

Rabat-Salé-Kénitra - 22,22% Dakhla-Oued Eddahab - 18,94%
L'Oriental - 22,22% Marrakech-Safi l 6,58%
Tanger-Tetouan-AI Hoceima - 11,11% L'Oriental l 4,51%
Tanger-Tetouan-AI 9
Marrakech-Safi - 11,11% Hoceima 0,15%
Investissement projeté Emplois

Rabat-Salé-Kénitra 43,97% Marrakech-Safi

L'Oriental - 30,79% Rabat-Salé-Kénitra

25,48%

Marrakech-Safi - 12,05% L'Oriental - 1,60%
Tanger-Tetouan-AI Hoceima - 9,64% Dakhla-Oued Eddahab ' 9,32%
9 Tanger-Tetouan-AI
Dakhla- }
akhla-Oued Eddatiab l 3,55% Hoceimg l 4,39%

L É


3.9 Secteur du Sport

Au cours du 1°" semestre de l’année 2024, 6 projets d’investissement au profit du secteur du
Sport ont été accordés sur un foncier de plus de 9 Ha, pour une valeur totale de l’ordre de
101 Mdh et devraient générer la création, à terme, de 168 emplois escomptés.

Presque 80% de la superficie mobilisée en faveur de ce secteur, est concentrée au niveau des
régions de l’Oriental et de Tanger-Tetouan -AI Hoceima.

=
Nbre Projets Superficie mobilisée

L'Oriental

Béni Mellal-Khénifra - 16.67% Béni Mellal-Khénifra ' 9,86%
Rabat Salé Kénitra - 16.67% Rabat-Salé-Kénitra ' 9,31%
Souss-Massa - 16,67% Souss-Massa | 0,10%

/
Investissement projeté Emplois

Tanger-Tetouan-AI

T -T« -AI

Hoceima
L'Oriental - 15,76% L'Oriental - 29,76%
Rabat-Salé-Kénitra l 3,05% Rabat-Salé-Kénitra l 5.95%
Béni Mellal-Khénifra l 1,97% Souss-Massa l 2,98%
Souss-Massa ‘ 0,44% Béni Mellal-Khénifra l 1,79%

A



IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

3.10 Secteur de la Santé

Au titre du 1°" semestre de l’année 2024, le secteur de la Santé a bénéficié de l’approbation de
6 projets d’investissement ayant pour support un foncier domanial d’une superficie globale de
l’ordre de 3 Ha, un investissement de 309 Mdh correspondant à la création, à terme, de 400
emplois escomptés.

79% de la superficie mobilisée est concentrée au niveau de la région de

Tanger-Tétouan -El Hoceima.

Nbre Projets Superficie mobilisée

Tanger-Tetouan-AI ;
Héâceims — d
16,67% Souss-Massa l 10,52%

Deraa- Tafilalet

Tanger-Tetouan-AI
Hoceima

Souss-Massa 16,67% L'Oriental

L'Oriental

Casablanca-Settat

16,67% Casablanca-Settat l 3,07%
16,67% Deraa tafilalet l

Investissement projeté

Souss-Massa — 64,72% Souss-Massa
Tanger-Tetouan-AI Tanger-Tetouan-Al
Hoceima - 25/80% Hoceima

Casablanca-Settat 3,88% Casablanca-Settat

Deraa- Tafilalet

L'Oriental

Derae-Tafilalel l 3,56%

L'Oriental



4. Déclinaison Régionale

La répartition régionale du foncier, fait ressortir, que :
» En termes de nombre de projets, ce sont les régions de Dakhla-Oued Eddahab, de
Laâyoune-Sakia El Hamra et de l’Oriental qui ont profité de 59% des projets approuvés,

au titre du 1” semestre de l’année 2024.

Nbre projets

Dakhla-Oued Eddohab I 2.55
Laäyoune-Sakia El Hamra E 22 75:
L'Oriental p E 11 5256
Tanger-Tetouan-Al Hoceima E s187
Casablonca-Settot E 65656
Fès-Meknès NNN 4559
Rabat-Salé-Kénitra NNN 4552
Guelmim-Oued Noun NNN 455%
Souss-Massa N 3.64%
Béni Mellal-Khénifra NNN 3.64%
Deraa- Tafilalet MM 2.73%

Marrakech-Safi IMN 2,73%

» Au cours de cette même période, c’est la région de Laâyoune-Sakia El Hamra qui

s'accapare plus de 95% de la superficie globale mobilisée.

Superficie mobilisée

Laävoune-Sakia El Hamra

Casablanca-Settat l 184%
Dakhla-Oued Eddahab [} 1.80%
Marrakech-Safi | 0,41%

Guelmim- Oued Noun | 0.35%
L'Oriental | 0.35%
Tanger-Tetouan-AI Hoceima | 0,10%
Rabat-Salé-Kénitra _ 0,09%

Autres 0.04%

d


IR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

» De même, les régions de Guelmim -Oued Noun et de Laâyoune-Sakia El Hamra ont
bénéficié de 80% des investissements, au titre du 1” semestre de l’année 2024.

Guelmim- Oued Noun
Laäyoune-Sakia El Hamra
Marrakech-Safi
Casablanca-Settat
Tanger-Tetouan-Al Hoceima
L'Oriental

Souss-Massa
Rabat-Salé-Kénitra
Dakhla-Oued Eddahab
Fès-Meknès

Béni Mellal-Khénifra

Deraa- Tafilalet

=
Investissement projeté

L rrr RL
PE s0.05
HE 50>

HE <0>

E 342>

| RE

E 16x

H 114%

H 104%

| 0.41%

| 0.13%

| 0,0%

» Encore plus, 60% des postes d’emploi à créer, sont concentrés au niveau de deux

régions : Casablanca- Settat et Tanger -Tétouan -El Hoceima.

Casablanca-Settat
Tanger-Tetouan-Al Hoceima
Rabat-Salé-Kénitra
L'Oriental
Laäyoune-Sakia El Hamra
Guelmim- Oued Noun
Dakhla-Oued Eddahab
Marrakech-Safi
Souss-Massa

Fès-Meknès

Béni Mellal-Khénifra

Deraa- Tafilalet

Emplois

—I 7
P 25 5>

E 7.56>

E 6.55::

E 655

E 226>

HE 1005

HE 156>

H 000%

| 0.32%

| 0.27%

L É


i PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 ‘

4.1 Laâyoune-Sakia El Hamra : Mobilisation du foncier en appui au secteur de l’Energie

Près de 15.301 Ha ont été mobilisés, par l'Etat (Domaine Privé), au titre du 1” semestre de l’année

2024, au niveau de la région de Laâyoune-Sakia El Hamra, bénéficiaire de 25 projets

d'investissement, dont le montant est de 5.092 Mdh permettant la création, à terme, de 1.094

emplois escomptés.

Au cours de cette période, c’est le secteur de

’Energie qui centralise la quasi-totalité de la

superficie globale mobilisée au niveau de cette région.

Nbre Projets

Services

/
Superficie mobilisée

Energie
Industrie ' 6.90%
Habitat | 212%
Services | 124%
Agro-industrie | 0.88%
Mines ‘ 0.45%
Enseignement et 0,04%

Formalion

Industrie - 16,00%
Mines l 133%
ut ME 16.00
Industrie | 0,27%
Agro-industrie - 12,00%
Habitat _ 0,19%
Mines - 8,00%
Enseignement et Agro-industrie _ 0,10%
Formation l s007
Energié l 4,00% Services . 0,02%
Investissement projeté Emplois

Agro-industrie

Services
Industrie

Mines

Enseignement et
Formation

Energie

A



IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

4.2 Casablanca-Settat : Mobilisation du foncier en faveur du secteur de l’Industrie

La région de Casablanca-Settat a capté 7 projets d’investissement, à réaliser sur des assiettes
foncières relevant du Domaine Privé de l’Etat, d’une superficie globale de 296 Ha, devant drainer
un investissement global de 724 Mdh et générer la création, à terme, de 6.230 emplois
escomptés.

Durant cette période, le secteur de l’Industrie a bénéficié, à lui seul, de 92% de la superficie
mobilisée au niveau de cette région.

Nbre Projets Superficie mobilisée
(nécsrie - 62606 (n —
Enseignement et 75 Enseignement et >
Formation - e Formation l 7.09%
Santé - 14,29% Santé 0.04%
Services - 14,29% Services … 0.02%
Investissement projeté Emplois
Industrie

s5 rs - SOTVE

Enseignement et Enseignement et
Formation - 3177% Formation #Q
Santé l 166% Santé | 0,80%
Services | 0,69% Services _ 0,40%

L É


4.3 Dakhla-Oued Eddahab: Mobilisation du foncier en appui aux secteurs des Mines et
de l’Agro-Industrie

L’Etat (Domaine Privé) a mobilisé, au niveau de la région de Dakhla-Oued Eddahab, des
assiettes foncières, d’une superficie globale de 290 Ha, au cours du 1°” semestre de l’année 2024,

destinées à recevoir 27 projets d’investissement.

Ces investissements d’une valeur totale de plus de 170 Mdh permettront la création, à terme, de
377 postes d’emploi, et profitent principalement aux secteurs des Mines et de l’Agro-Industrie

avec un pourcentage de 97% de la superficie mobilisée au niveau de cette région.

Nbre Projets Superficie mobilisée )
Services — 40.74% Mines —48.90%
Industrie 18.52% Agro-industrie — 48,28%
Agro-industrie 18,52% Services l 120%
Tourisme 11,11% Tourisme l 102%
Mines 11,11% Industrie | 0,60%
, %
Investissement projeté Emplois
Agro-industrie 48,32% | | Agro-industrie
Industrie - 18,39% Services 25,46%
Services - 16.66% Industrie 21,75%
Mines - 13,18% Tourisme 14,06%
Tourisme I 3,45% Mines 11,94%

A



R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

4.4 Marrakech-Safi : Mobilisation du foncier en faveur du secteur des Services

La région de Marrakech-Safi a bénéficié, au titre du 1” semestre de l'année 2024, de la
mobilisation d'une superficie de 65 Ha, destinée à recevoir 3 projets d’investissement
principalement dans le secteur des Services, d’une valeur totale de plus de 740 Mdh
correspondant à la création, à terme, de 333 emplois escomptés.

Superficie mobilisée

Nbre Projets

Tourisme

Services 33,33% Tourisme | 152%

Agro-industrie 33,33%| | Agro-industrie

1,45%

Investissement projeté Emplois

Agro-industrie

Tourisme

2,70% Agro-industrie - 15,02%

0,80%

Services | 0,07% Services

L É


4.5 Gue/mim-Oued Noun : Mobilisation du foncier en faveur du secteur de l’Industrie

La région de Guelmim-Oued Noun a enregistré, au titre du 1°" semestre de l’année 2024, la
mobilisation d’une superficie globale de 56 Ha, dédiée à la réalisation de 5 projets

d’investissement, d’une valeur totale de 8.090 Mdh correspondant à la création de 1.086 postes
d'emploi.

68% de la superficie mobilisée au niveau de cette région, est destinée à recevoir 3 projets

d'investissement dans le secteur Industriel, pour une enveloppe globale de l’ordre de 8.014 Mdh.

Nbre Projets Superficie mobilisée
Industrie - 60,00% ladustrie
Services . 20,00% Acro-industrie 8,91%
Agro-industrie ' 20,00% Services | 0.52%

Investissement projeté

Emplois
_ - ts Pers
Agro-industrie | 0,85% Acro-industrie 5,52%
Services | 0,09% Services | 0854

pN



R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

4.6 L’Oriental : Mobilisation du foncier en appui au secteur de l’Agro-Industrie

Au cours du 1” semestre de l’année 2024, l’Etat (Domaine Privé) a mobilisé, au niveau de la
région de l’Oriental, une superficie globale de plus de 55 Ha (dont plus de 83% au profit du

secteur de l’'Agro-industrie), destinée à recevoir 13 projets d’investissement.

Ces investissements d’une valeur globale de plus de 519 Mdh correspondant à la création, à
terme, de 1.316 postes d'’emploi, portés, essentiellement, par le secteur des Mines.
Nbre Projets Superficie mobilisée
Industrie — 23,08% Acro-induslrie —8354%
Agro-industrie — 25,08% Santé ' 7,22%
Tourisme — 15,38% Sporl l 6,42%
sport NNN 5.55:; Services | 127%
Services - 7,69% Mines | 0,91%
santé N 7.50 lndustrie | 0,45%
Mines M 7.60 Tourisme | 019%
Investissement projeté Emplois
Tourisme - 9,85% Agro-industrie - 7,60%
Agro-industrie ' 7,95% Tourisme I 5,02%
Sport l 3.08% Industrie I 4,55%
Industrie | 141 Sport }} 380%
santé l 116% Services l 190%
Services l 0,67% aante l J2

L É


4.7 Tanger-Tétouan-AI Hoceima : Mobilisation du foncier en faveur du secteur de
l’Enseignement et de la Formation

Au titre du 1°" semestre de l’année 2024, 9 projets d’investissement ayant pour support un
foncier domanial, au niveau de la région de Tanger-Tétouan-AI Hoceima, ont été approuvés,
pour une superficie globale de 16 Ha.

Ces projets d’investissement d’une valeur totale de plus de 563 Mdh, devraient générer, à terme,

la création de 3.930 postes d’emploi.
Presque 42% de la superficie mobilisée au profit de cette région, est dominée par le secteur de
’Enseignement et de la Formation.
Nbre Projets Superficie mobilisée
Ensa es - 22.23% Sport - 22,47%
Tourisme - M,119€ Santé - 18,70%
Sport - T1,11% Industrie - 17.08%
Santé - TL119é Tourisme | 0,14%
Investissement projeté Emplois
Tourisme — 47,91% Industrie — 81,42%
Industrie - 20,86% Eosénementes ' 12,85%
Sport - 14,20% Sport l 2,54%
Santé - 14,20% Santé l 2,54%
EnSÊÊÎÊÊÎ}Ï « l 2,83% Tourisme ’ 0,65%

A



R LE FONCIER PUBLIC MOB

E POUR L’INVESTISSEMENT

4.8 Rabat-Salé-Kénitra : Mobilisation du foncier en faveur du secteur du Tourisme

Au niveau de la région de Rabat-Salé- Kénitra, l’Etat (Domaine Privé) a mobilisé une superficie
globale de plus de 14 Ha, au profit de 5 projets d’investissement, pour une enveloppe globale
de 187 Mdh correspondant à la création, à terme, de 1.820 postes d’emploi.

Plus de 76% de la superficie mobilisée au profit de cette région, est dominée par le secteur du

Tourisme.

Nbre Projets Superficie mobilisée

606 Tovrsme - m0s

20% Agro-induslrie ' 13,91%
20% Sport l 6,11%

Tourisme

Sport

Enseignement et
Formation

Enseignement et

Agro-industrie 20% Formation 3,52%

Investissement projeté Emplois
Agro-industrie - 48,59% Agro-industrie -82,42%
Tourisme - 38.85% Enséeneigentet l 907%
an:gg£]æäräzgt et ' 10,91% Tourisme l 7,97%
Sport l 1,65% Sport | 0,554%

L É


4.9 Fès- Meknès : Mobilisation du foncier en appui au secteur de l’Industrie

Au titre du 1” semestre de l’année 2024, la région de Fès-Meknès a capté 5 projets à réaliser sur
des assiettes foncières d’une superficie de 4,5 Ha, devant drainer un investissement d’environ
68 Mdh et générer la création, à terme, de 150 postes d’emploi.

La quasi-totalité de la superficie mobilisée au niveau de cette région, est allouée au secteur de
’Industrie (Unités de production des matériaux de construction).

Nbre Projets Superficie mobilisée

pocre — (On ps - 96065

Services - 20% Services l 3,98%

Investissement projeté Emplois

mts - v meverre —

Services l 3,28% Services I 6,67%

yN



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

4.10 Béni Mellal-Khénifra : Mobilisation du foncier en appui au secteur du Sport

Cette région a pu accrocher 4 projets d’investissement, envisagés sur un foncier domanial, d’une
superficie totale d’un hectare (1 ha), devant drainer un investissement de l’ordre de 20 Mdh et

générer la création, à terme, de 53 postes d’emploi.

Nbre Projets Superficie mobilisée

Services Sport

Sport 25% Services 12,55%

Investissement projeté Emplois

P — v

Sport l 9,85% Sport l 5,66%

L É


4.11 Souss -Massa : Mobilisation du foncier en appui au secteur de la Santé et de la
Culture

Au cours du 1” semestre de l'année 2024, la région de Souss-Massa a enregistré la mobilisation
d’une superficie globale de 9.359 m°, destinée à recevoir 4 projets d’investissement, pour une
enveloppe globale de plus de 270 Mdh permettant la création, à terme, de 260 postes d’emploi.

Nbre Projets Superficie mobilisée

Culture — 25% Culture - 28,60%

Services — 25% Services - 27,47%
#
Investissement projeté Emplois

Santé b santé

Culture - 21,45% Culture . 15,38%
Services l4,43% Services l 5,77%

Sport | 0,17% Sport l1,93%



4.12 Deräa -Tafilalet : Mobilisation du foncier en appui au secteur des Services

Au cours du 1” semestre de l’année 2024,
mobilisation d’une superficie globale de 1.070 m

pour une enveloppe globale de 17 Mdh permettant la création, à terme, de 45 postes d'’emploi.

a région de Derâa -Tafilalet a enregistré
2

, destinée à recevoir 3 projets d'investissement.

Nbre Projets

Santé 66,67%

Superficie mobilisée

Ps

Investissement projeté Emplois
E — PU ue — .
Services - 35,29% Services - 22,22%

E POUR L’INVESTISSEMENT

9

L É


Il. MOBILISATION DU FONCIER DANS LE CADRE DU PARTENARIAT
AGRICOLE - 1°" SEMESTRE 2024 -

1. Données globales

Au titre du 1 semestre de l’année 2024, 44 conventions ont été signées dans le cadre du
Partenariat Agricole, suite aux appels d’offres organisés à cet effet, portant sur une superficie
de plus de 935 Ha, un investissement global de plus de 615 Mdh et permettant la création, à

terme, de 2.309 postes d’emploi.

Fès-Meknès 331ha56a13ca 43 757 270 214
Dakhla-Oued Eddahab 242ha46al5ca 598 776 907 1.654
Laâyoune -Sakia El Hamra 133ha44a33ca 108 374 357 248

103ha63a02ca 15 398 367 31
49ha76a33ca 20 609 293 60
38ha3la93ca 9917 692 41
21ha30al6ca 4 926 800 27

Casablanca-Settat O9ha81a00ca 8110 000 11

Tanger-Tétouan-AI Hoceima O5ha54al6ca 5 973 000

2
6
7
1
|
1

A signaler qu’un appel d’offre n°31/2024 a été lancé par l’Agence du Développement Agricole

L'Oriental
Béni Mellal-Khénifra
Rabat-Salé-Kénitra
Marrakech-Safi

(ADA) portant sur des terrains relevant du domaine privé de l’Etat. La date limite de dépôt des

offres par les candidats est fixée pour le lundi 30 septembre 2024.
Cet appel d'offres qui porte sur 96 projets et une superficie globale de 5.249 Ha concerne

les régions ci-après :

Superficie en Ha

Casablanca-Settat
Deräa-Tafilalet
Fès-Meknès
Marrakech-Safi
Tanger-Tétouan-AI Hoceima
Rabat-Salé-Kénitra

Oriental

Souss-Massa

Béni Mellal-Khénifra

Total général



2. Ventilation par filière

Au titre du 1” semestre de l'année 2024, les fi

IR LE FONCIER PUBLIC MOI

SE POUR L’INVESTISSEMENT

ières de Maraîchage, de l'Agrumiculture et de

l’Arboriculture fruitière ont bénéficié d’environ 76% de la superficie mobilisée au profit des

projets d’investissement dans le cadre du Partenariat Agricole.

p
Nbre projets pn Superficie louée
5 4,55% O6/% — 2,58%
— 4,55% |
. 10.15%
18.18%
21,21%
20,45% sp
» Autres production végétales » Autres production végétales
Viticulture Viticulture
Agrumiculture Production animale
= Maraîchage = Oliéculture
Oliéculture Agrumiculture
Arboriculture Arboriculture
= Production animale k « Maralchage
Investissement projeté 104% Emplois ,-2.08%
098%\‘r77% 2.59% \]91%/4.37%
| Â,AT% l 4,50%
[ 6,46%

6,94%

» Autres production végétales
Viticulture
Oliéculture

= Agrumiculture
Arboriculture
Production animale

= Maraîchage

7,49%

» Autres production végétales
Oliéculture
Viticulture

= Arboriculture
Production animale
Agrumiculture

= Maraîchage



2.1 Maraîchage

Au cours du 1” semestre 2024, l’Etat (Domaine privé) a mobilisé 304 Ha au profit de la filière
du Maraichage, soit environ 33 % de la superficie globale mobilisée, bénéficiant aux 4 projets,
pour un investissement total d’une valeur de plus de 473 Mdh correspondant à la création de

1.815 postes d’emploi.

La région de Dakhla -Oued Eddahab a enregistré, à elle seule, environ 80 % de la superficie

mobilisée au profit de cette filière (1.247 Ha).

Superficie louée

Laâyoune Sakia El Hamra - 20,58%

2.2 Agrumiculture

L'Etat (DPE) a loué 198 Ha au profit de 2 projets dans la filière de l'Agrumiculture, localisé au
niveau de la région de Fès-Meknès, bénéficiant, d’environ 21% de la superficie globale mobilisée,
au titre du 1” semestre de l’année 2024, pour un investissement global de 27 Mdh et générant

la création de 173 emplois escomptés.

2.3 Arboriculture fruitière

Au cours du 1” semestre de l’année 2024, 9 conventions ont été signées au profit de la filière
de l'Arboriculture fruitière, bénéficiant, d’environ 22 % de la superficie globale mobilisée
(207Ha), pour une enveloppe globale d’environ 40 Mdh permettant la création de 101 postes

d’emploi.

La région de l’Oriental profite, à elle seule, d’environ 46 % de la superficie mobilisée au profit de
cette filière.

Superficie mobilisée

L'Oriental 45,84%

Béni Mellal-Khénifra 21,08%

Fès-Meknès 19:31%

Rabat-Salé-Kénitra

pN

13,77%



3. Déclinaison Régionale

RAPPORT SUR LE FONCIER PUBLIC MOI SE POUR L’INVESTISSEMENT

La répartition régionale des conventions signées, au titre du 1°" semestre de l’année 2024, fait

ressortir que :

> Plus de 84% des projets approuvés sont concentrés au niveau de 4 régions:
Laâyoune -Sakia El Hamra, Fès-Meknès, Rabat- Salé -Kénitra et Béni Mellal-Khénifra.

> Au cours de cette période, les régions de Fès-Meknès, Dakhla-Oued Eddahab,
Laâyoune -Sakia El Hamra et l'Oriental ont enregistré la mobilisation d’environ 87% de la
superficie globale allouée au profit des projets d’investissement dans le cadre du

Partenariat Agricole.

Nb projets

Laäyoune Sakia E| Harnra NN
Fès-Meknès NNN 18.16%
Rabat-Salé-Kénitra IRRN 15.019
Béni Mellal-Khénifra MEN 13,64%

Dakhla-Oued Eddahab [} 4,55%
L'oriental f 4.55%
Marrakech-Safi [} 2.27%

Casablanca-Settat [} 2.27%

p=
Superficie louée

Fès-Meknès
Dakhla-Oued Ecdahalb e 25.0155
L'aäyoune Sakia Fl Harmra MEN 14.26%
L'criental - 1,06%

Béni Mellal Khénifra [} 5.32%
Rabat-Salé-Kénitra [ 4.09%
Marrakech-Safi [} 228%

Casablanca-Settat | 105%

Dakhla-Oued Eddahab

Laäyoune Sakia El Hamra - 17,60%
Fès-Meknès B} 71%
Béni Mellal-Khénifra } 3,35%
L'oriental I 2,50%
Rabat-Salé-Kénitra | 1,61%
Casablanca-Settat | 132%
Tanger-Tetouan-Al..| 0,96%

Marrakech-Safi | 0.80%

Tanger-Tetouan-Al D Tanger-Tetouan-AI x
Hoceima H 227% oceiia | 0.60%
Investissement projeté Emplois

Dakhla-Oued Eddahab _

Laäyoune Sakia El Hamra [} 10.74%
Fès-Meknès } 9.27%
Béni Mellal-Khénifra | 260%
Rabat-Salé-Kénitra | 1,78%
L'eriental | 134%
Marrakech-Safi | 117%
Tanyger-Telouan-Al..| 1,00%

Casablanca-Settat | 0,47%

L É


3.1 Fès-Meknès (Agrumiculture)

La région de Fès -Meknès a bénéficié de la conclusion de 8 conventions d’investissement dans
le cadre du Partenariat Agricole, au titre du 1” semestre de l'année 2024, portant sur des
terrains, d’une superficie globale de 331 Ha, affectés principalement à l'Agrumiculture.

Ces conventions d’investissement d’une valeur globale de plus de 43 Mdh vont permettre la
création, à terme, de 214 postes d’emploi.

( D
Nbre projets Superficie louée
0.87%
12,07%
27,19%
25,00%
« Viticulture Agrumiculture = Viticulture Arboriculture
Arboriculture = Oliéculture Oliéculture — = Agrumiculture
Investissement projeté Emplois
264% 1,40%
7,94%
13,71%
9,81%
21,53%
= Arboriculture — Viticulture = Arboricullure - Oliécullure
Oliéculture — « Agrumiculture Viticulture = Agrumiculture

pN



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

3.2 Dakhla-Oued Eddahab (Maraîchage)

La région de Dakhla-Oued Eddahab a bénéficié de la conclusion de 2 conventions
d'investissement dans le cadre du Partenariat Agricole, au titre du 1°" semestre de l’année 2024,
portant sur des terrains, d’une superficie globale de 242 Ha, dédiés à la Culture maraîchère.

Ces conventions d’investissement d’une valeur globale de plus de 398 Mdh vont permettre la

création, à terme, de 1.654 postes d’emploi.

3.3 Laâyoune -Sakia El Hamra (Production animale et Maraîchage)

La région de Laäyoune -Sakia El Hamra a bénéficié de la signature de 16 conventions
d'investissement dans le cadre du Partenariat Agricole, au titre du 1°" semestre de l’année 2024,
portant sur des terrains, d’une superficie globale de 133 Ha, affectés à la Production animale
et à la Culture maraîchère.

Ces conventions d’investissement d’une valeur globale de 108 Mdh vont permettre la création,
à terme, de 248 postes d’emploi.

Nbre projets Suoerficie louée

12%

47%

Maraîchage " Production animale Maraîchage = Production animale

Investissement projeté Emplois

51%

= Maraîchage Production animale « Maraîchage Production animale



3.4 L’Oriental (Arboriculture fruitière)

La région de l’Oriental a bénéficié, au titre du 1°" semestre de l'année 2024, de 2 conventions
d’investissement dans le cadre du Partenariat Agricole, à réaliser sur des assiettes foncières,
d'une superficie globale de plus de 103 Ha, favorisant la filière de l’Arboriculture fruitière, pour

un investissement projeté de 15 Mdh et permettant la création, à terme, de 31 emplois
escomptés.

Nbre projets Superficie louée

9,01%

= Arboriculture fruitière » Production animale

# Arboriculture fruitière » Production animale

Investissement projeté Emplois

2,07%

3,23%

= Arboriculture fruitière » Production animale

« Arboriculture fruitière » Production animale

pN



RAPPORT SUR LE FONCIER P!

3.5 Béni Mellal -Khénifra (Arboriculture fruitière)

SE POUR L’INVESTISSEMENT

La région de Béni Mellal -Khénifra a bénéficié, au titre du 1°" semestre de l’année 2024, de

6 projets d’investissement dans le cadre du Partenariat Agricole, devant être réalisés sur des

assiettes foncières, d'une superficie globale d’environ 50 Ha, destinés en partie à

l’Arboriculture fruitière, pour un investissement projeté de plus de 20 Mdh et permettant la

création, à terme, de 60 emplois escomptés.

Investissement projeté

O.17\%\6,7o%

Autres production végétales
Oliéculture
= Arboriculture fruitière

Nbre projets Superficie louée
%
0,47%4,56% _s

1102%

Autres production végétales Autres production végétales

Arboriculture fruitière Oliéculture

= Oliéculture = Arboriculture fruitière
P

Emplois
1,67%

Autres production végétales
Oliéculture

= Arboriculture fruitière



| PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 ‘

3.6 Rabat-Salé-Kenitra (Arboriculture fruitière)

La région de Rabat-Salé-Kénitra a bénéficié, au titre du 1" semestre de l’année 2024, de

7 projets d’investissement dans le cadre du Partenariat Agricole, destinés en part à

l’Arboriculture fruitière (environ 75% de la superficie mobilisée au niveau de cette région),

devant être réalisés sur des assiettes foncières, d’une superficie globale de plus de 38 Ha, pour

un investissement projeté d’environ 10 Mdh et permettant la création, à terme, de 41 emplois

escomptés.

Nbre projets

14,29%

14,29%

Oliécullure » Produclion animale = Arboricullure

Superficie louée

12,02%

13,52%

Cliécullure Produclion animale

« Arboriculture

Investissement projeté

3,93%

44,10%

Production animale » Arboriculture = Oliéculture

Emplois

12,20%

24,39%

Production animale » Oliéculture # Arboriculture

VN



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

3.7 Marrakech-Safi (Viticulture)

Au cours du 1°" semestre de l’année 2024, la région de Marrakech-Safi a bénéficié d’un seul
projet d’investissement dans le cadre du Partenariat Agricole, destiné à la Viticulture, devant
être réalisé sur une assiette foncière, d'une superficie de 21 Ha, pour un investissement projeté
d’environ 5 Mdh et permettant la création, à terme, de 27 emplois escomptés.

3.8 Casablanca -Settat (Production animale)

Au titre du 1” semestre de l’année 2024, la région de Casablanca-Settat a bénéficié
d’'un seul projet d’investissement dans le cadre du Partenariat Agricole, à réaliser
sur un foncier domanial, d’une superficie de plus de 9 Ha, affecté à la Production
animale, avec un investissement global de plus de 8 Mdh permettant la création, à

terme, de 11 emplois escomptés.

3.9 Tanger- Tétouan- Al Hoceima (Arboriculture fruitière)

Au niveau de la région de Tanger-Tétouan-AI Hoceima, un seul projet d’investissement a été
approuvé dans le cadre du Partenariat Agricole, au titre du 1" semestre de l’année 2024, à
réaliser sur une superficie d’environ 6 Ha, destiné à l’Arboriculture fruitière.

Ce projet devrait drainer un investissement global de l’ordre de 6 Mdh et générer la création,
à terme, de 23 postes d’emploi.



Mobilisation du foncier pour l'Investissement -Année 2023 -

“ Nb de projets Superficie mobilisée lnveshsse(r;‘:;‘( Projoté Emploi escompté

ce n Déconcent ce 466 13.438ha16a74ca 37.830.276.19 20.474
de l’Investissement

Total gé a74c @ 5
Dakhla-Oued Eddahab 1.120ha 21a 13ca 5.048.025.000 6 281
Laäyoune-Sakia El 99 N845ha O7a 10ca 21,960.122.000 27
lérearlé se 29 289ha 27a 27ca 8.165.022.000 4 621
Hoceima
Guelmim-Oued Noun 15 72ha 82a 58ca 432.404.319 534
Rabat-Salé-Kénitra 8 37ha 73a 85ca 325.332.9317 2651
Casablanca-Settat 12 29ha 86a 89ca 656.914.740 1116
L'Oriental 43 26ha 55a 09ca 867.907.600 1897
Marrakech-Safi 5 Obha 99a O5ca 99.770.000 124
Souss-Massa S O6ha 5la 63ca 135.060.000 210
Fès-Meknès 1 O2ha 37a O9ca 20.000.000 30
Deréa-Tafilalet 1 OOha 38a 24ca 98.000.000 84
Béni Mellal-Khénifra 2 OOha 36a 84ca 21.717.543 55

38hal6a74 119 20.474

Total général

Investissement
“ Nb de projets Superficie mobilisée projeté (dh) Emploi escompt

Energie 7.168ha 51a 44ca 5:13.500.000
Mines 35 4.006ha 48a 24ca 18.879.714.000 846
Habitat 4 836ha 50a 58ca 3.706.383.000
ps es 4 468ha 52a 92ca 34.560.000 68
d'activité
Industrie 94 452ha OOa 72ca 4.,460.692.374 7.981
Agro-industrie 55 22Zha 63a 68ca 1.431.713.740 2.246
Tourisme 120 187ha 36a 28ca 2.433.809.600 4,988
Services 84 69ha 40a 42ca 616.130.262 1850
sc armen 16 13ha 64a 23ca 169.117.600 551
Formation
Sport 9 O9ha 40a O3ca 70.335.543 498
Santé 7 Olha 68a 20ca 914.320.000 1.046

MEN



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

Mobilisation du foncier dans le cadre du partenariat agricole
-Année 2023-

Fès-Meknès 49 2.256ha 27a O3ca 193359 727 341
Tanger-Tétouan-AI Hoceima S 528ha O8a 54ca 146.578.540 175
Casablanca-Settat 10 437ha O4a 77ca 159.172.551 290
Rabat-Salé-Kénitra KY4 248ha 73a O4ca 124.286.089 267
Béni Mellal-Khénifra 26 139ha 13a O4ca 24.579.767 83
Souss-Massa 2 126ha 17a 84ca 12/875:328 2
L'Oriental 22 89ha 87a O8ca 41.153.828 127
Laâyoune -Sakia el Hamra 5 15ha 68a 47ca 4.095.000 17

Total général 179



Mobilisation du foncier pour l'Investissement - 1°" semestre de l’année 2024 -
8 | nent Emploi

Laâyoune-Sakia El Hamra 25 15.301he 37a 78ca 5.092.260.000 1.094
Casablanca-Settat 7 296ha O5a 30ca 724.000.000 6.230
Dakhla-Oued Eddahab 27 290ha 36a 48ca 170.918.000 s7
Marrakech-Safi 3 6Sha 89a 52ca 740.500.000 335
Guelmim-Qued Noun 5 S56ha 13a 49ca 8.090.324.803 1086
L'Oriental 13 55ha 7la 34ca 519.220.525 1.316
Tanger-Tétouan-AI Hoceima 9 16ha O3a 44ca 563.535.499 35.950
Rabat-Salé-Kénitra S 14ha 38a 59ca 187.900.000 1.820
Fès-Meknès 5 O4ha 53a 73ca 67.980.000 150
Béni Mellal-Khénifra 4 Olha O6a 54ca 20.310.000 55
Souss-Massa 4 OOha 93a 59ca 270.450.000 260
Deräa-Tafilalet 3 OOha 10a 70ca 17.000.000
m=N
(le semestre 2024)

ie mobi

Energie 1 15.009 ha O0a OOca _ 4.500.000.000
Mines 6 392ha 13a 20ca 439.310.000 bere
Industrie 26 375ha 48a 90ca 9.064 555.499 12645
Agro-industrie 14 166ha 27a 20ca 1048.952.500 Cts
Services 31 72ha 99a 71ca 146.424.803 .
Habitat 4 29ha 23a 37ca 108.080.000
Enseignement et Formation 6 28 ha24a 34ca 522.500.000 820
lourisme 9 I5ha /0a 88ca 166.026.025 s.
Sport 6 9 ha44a 81ca 101.550.000 e
Santé 6 3ha 8la 32ca 309.000.000 s0
Culture Il 26a 77ca 58.000.000 40

Total général 10
(1ë semestre 2024) ;



RAPPORT SUR LE FONCIER PUBLIC MOBILISE POUR L’INVESTISSEMENT

Mobilisation du foncier dans le cadre du partenariat agricole

- 1ë" semestre de l’année 2024 -

Montant
Conventions
Région Superficie Investissement | Emplois
établies vn
(dh)
214

Fès-Meknès 31ha 56a 13ca 43.757.270
Dakhla-Oued Eddahal 2 242ha 46a 15ca 398.776.907 1654
Leéyoune Selia E 16 133ha 44a 33ca __ 108.374.357 248
Hamra

L'Oriental 2 103ha 63a O2ca 18:398.567 3I

Béni Mellal-Khénifra 6 49ha 76a 33ca 20.609.293 60

Rabat-Salé-Kénitra 7 38ha 31a 93ca 9.917.692 41

Marrakech-Safi 1 21ha 30a 16ca 4.926.800 27

Casablanca-Settat 1 O9ha 81a OOca 8.110.000 11

JéneetEnsA OSha 64a l6ca — 5.973.000
Hoceima

Total général
935ha93a21ca 615.843.686
SE oucaus 20250 --

"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("PLF2025: Explorez le rapport sur le foncier public mobilise pour l'investissement à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

        # Afficher toujours la barre de saisie
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
    selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
    query_input = st.text_input("", key="text_input_query", placeholder="Posez votre question ici...", help="Posez votre question ici...")
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

    if query_input and query_input not in st.session_state.previous_question:
        query = query_input
        st.session_state.previous_question.append(query_input)
    elif selected_questions:
        query = selected_questions
    else:
        query = ""

    if query :
        st.session_state.conversation_history.add_user_message(query) 
        if "Donnez-moi un résumé du rapport" in query:
            summary="Le document « Rapport sur le foncier public mobilisé pour l’investissement », dans le cadre du Projet de Loi de Finances 2025, traite de la mobilisation des terrains publics en faveur des projets d'investissement. Il met en lumière l’importance stratégique de ces biens fonciers pour stimuler l’investissement, soutenir l’économie nationale et favoriser le développement de projets à haute valeur ajoutée. Ce rapport présente également les mesures entreprises pour optimiser l’utilisation de ces terres, tout en garantissant une gestion transparente et efficace de ce patrimoine public."
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte donnee des réponse significatif et bien formé essayer de ne pas dire que information nest pas mentionné dans le texte si tu ne trouve pas essayer de repondre dapres votre connaissance ms focaliser sur ce texte en premier: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

            summary = response['choices'][0]['message']['content']
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary)  # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
            # Format et afficher les messages comme précédemment
        formatted_messages = []
        previous_role = None 
        if st.session_state.conversation_history.messages: # Variable pour stocker le rôle du message précédent
                for msg in conversation_history.messages:
                    role = "user" if msg.type == "human" else "assistant"
                    avatar = "🧑" if role == "user" else "🤖"
                    css_class = "user-message" if role == "user" else "assistant-message"

                    if role == "user" and previous_role == "assistant":
                        message_div = f'<div class="{css_class}" style="margin-top: 25px;">{msg.content}</div>'
                    else:
                        message_div = f'<div class="{css_class}">{msg.content}</div>'

                    avatar_div = f'<div class="avatar">{avatar}</div>'
                
                    if role == "user":
                        formatted_message = f'<div class="message-container user"><div class="message-avatar">{avatar_div}</div><div class="message-content">{message_div}</div></div>'
                    else:
                        formatted_message = f'<div class="message-container assistant"><div class="message-content">{message_div}</div><div class="message-avatar">{avatar_div}</div></div>'
                
                    formatted_messages.append(formatted_message)
                    previous_role = role  # Mettre à jour le rôle du message précédent

                messages_html = "\n".join(formatted_messages)
                st.markdown(messages_html, unsafe_allow_html=True)
if __name__ == '__main__':
    main()

