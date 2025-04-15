# **📱 AHP System - Documentation**

---

## **🌐 Aperçu du Projet**
**AHP System** est une application web Django qui utilise la méthode **Analytic Hierarchy Process (AHP)** pour aider les utilisateurs à choisir la meilleur option en fonction de leurs préférences personnelles, parmis une gamme de propositions.  

L'application propose deux modes :
1. **Mode Rapide** : Utilise des données pré-définies (du cours) pour une analyse instantanée.
2. **Mode Personnalisé** : Permet à l'utilisateur de définir ses propres critères, alternatives et comparaisons par paires.

---

## **🚀 Fonctionnalités**
✅ **Comparaison par paires** avec l'échelle de Saaty (1-9 et leurs inverses)  
✅ **Calcul automatique** des poids des critères et du ratio de cohérence  
✅ **Classement complet** des alternatives avec scores détaillés  
✅ **Meilleur choix recommandé** basé sur l'analyse AHP  
✅ **Interface intuitive** avec Bootstrap 5  

---

## **⚙️ Installation**

### **Prérequis**
- Python 3.8+
- pip
- Git (optionnel)

### **1. Cloner le dépôt**
```bash
git clone https://github.com/Noubissie237/ahp_project.git
cd ahp_project
```

### **2. Créer un environnement virtuel**
```bash
python3 -m venv .ahp_venv
source .ahp_venv/bin/activate  # Linux/Mac
.ahp_venv\Scripts\activate    # Windows
```

### **3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

### **4. Migrer la base de données**
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

### **5. Lancer le serveur de développement**
```bash
python manage.py runserver
```
L'application sera accessible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## **📊 Utilisation**

### **Mode Rapide (Exercice du cours)**
1. Accédez à la page d'accueil.
2. Cliquez sur **"Mode rapide"**.
3. Consultez les résultats instantanés basés sur des données pré-définies.

### **Mode Personnalisé**
1. Accédez à la page d'accueil.
2. Cliquez sur **"Créer un AHP Personnalisé"**.
3. Ajoutez vos **critères** (ex: Mémoire, Prix, Marque, etc).
4. Ajoutez vos **alternatives** (ex: iPhone 15, Samsung S23).
5. Comparez les critères par paires en utilisant l'échelle de Saaty.
6. Évaluez chaque alternative selon les critères.
7. Visualisez le **classement final** et le **meilleur choix**.

---

## **📁 Structure du Projet**
```
ahp_project/
├── ahp_app/
│   ├── models.py          # Modèles de données (Critères, Alternatives, etc.)
│   ├── views.py           # Logique des vues (Mode Rapide/Personnalisé)
│   ├── ahp_calculator.py  # Calculs AHP
│   └── templates/         # Templates HTML
├── ahp_project/
│   ├── settings.py        # Configuration Django
│   └── urls.py           # Routes de l'application
├── requirements.txt       # Dépendances Python
└── README.md             # Documentation
```

---

## **🔧 Personnalisation**
Pour modifier les données par défaut (Mode Rapide), éditez :
```python
# Dans ahp_app/views.py (QuickModeView)
static_data = {
    'criteria': ['Mémoire', 'Stockage', 'Prix', ...],
    'alternatives': ['iPhone 12', 'Samsung S22', ...],
    'criteria_comparison': [...],
    'performance_matrix': [...]
}
```

---


## **📬 Contact**
Pour toute question ou suggestion, contactez :  
✉️ [wilfried.noubissie@facsciences-uy1.cm](mailto:wilfried.noubissie@facsciences-uy1.cm)  
🌍 [https://github.com/Noubissie237](https://github.com/Noubissie237)

---

<div align="center">
    <p>✨ <strong>Merci d'utiliser AHP System !</strong> ✨</p>
</div>

---