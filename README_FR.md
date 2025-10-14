# Keep Claude Code Busy

> **[中文](README.md) | [English](README_EN.md) | Français | [日本語](README_JA.md) | [Español](README_ES.md)**

Un outil de surveillance de région d'écran Windows conçu pour maintenir Claude Code actif pendant que vous dormez.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Plateforme](https://img.shields.io/badge/plateforme-Windows-lightgrey.svg)
![Licence](https://img.shields.io/badge/licence-MIT-orange.svg)

## ✨ Fonctionnalités

- ✅ **Sélection Visuelle de Région** - Dessinez un rectangle pour sélectionner la zone de surveillance
- ✅ **Surveillance en Temps Réel** - Détecte les changements d'écran par comparaison d'images
- ✅ **Détection Intelligente** - Se déclenche automatiquement après 30-120 secondes sans changement
- ✅ **Messagerie Automatique** - Envoie automatiquement des commandes à Claude Code
- ✅ **Persistance de Configuration** - Mémorise vos paramètres (optionnel)
- ✅ **Sortie Propre** - Arrêtez la surveillance à tout moment au réveil
- ✅ **Package en Un Clic** - Créez un fichier EXE autonome

## 🚀 Démarrage Rapide

### Installation

1. **Installer les dépendances**:
```bash
install.bat
```
ou manuellement:
```bash
pip install -r requirements.txt
```

2. **Exécuter le programme**:
```bash
python monitor_tool.py
```
ou double-cliquez sur `run.bat`

### Créer un EXE (Recommandé)

```bash
build_onedir.bat
```

L'exécutable sera dans `dist/monitor_tool/monitor_tool.exe`

## 📖 Comment Utiliser

### Étape 1: Sélectionner la Région de Surveillance

1. Cliquez sur le bouton "选择区域" (Sélectionner la Région)
2. L'écran devient semi-transparent
3. **Glissez** pour dessiner un rectangle autour de la zone de sortie de Claude Code
4. **Appuyez sur Entrée** pour confirmer (ou ESC pour annuler)

### Étape 2: Sélectionner la Position de Clic

1. Après avoir confirmé la région, l'écran reste semi-transparent
2. **Cliquez** sur l'emplacement du champ de saisie de Claude Code
3. **Appuyez à nouveau sur Entrée** pour confirmer

### Étape 3: Configurer les Paramètres

- **Intervalle de Vérification**: Fréquence de vérification des changements (10-60s, défaut: 30s)
- **Temps de Déclenchement**: Durée sans changement avant déclenchement (30-120s, défaut: 45s)
- **Seuil de Similitude**: Strictesse de comparaison d'images (0.90-0.99, défaut: 0.98)
- **Mémoriser la Position**: Restaurer automatiquement la région au prochain démarrage (case à cocher)
- **Message**: Texte à envoyer lors du déclenchement (supporte le chinois)

### Étape 4: Démarrer la Surveillance

Cliquez sur le bouton "开始监控" (Démarrer la Surveillance) et allez dormir! 😴

### Étape 5: Arrêter au Réveil

Cliquez sur le bouton "停止监控" (Arrêter la Surveillance) ou fermez la fenêtre.

## 🎯 Fonctionnement

1. Prend des captures d'écran de la région surveillée toutes les N secondes
2. Compare la capture actuelle avec la précédente
3. Si des changements sont détectés → réinitialiser le minuteur
4. Si AUCUN changement pendant M secondes → automatiquement:
   - Cliquer sur le champ de saisie
   - Coller le message avec Ctrl+V (supporte le chinois)
   - Appuyer sur Entrée pour envoyer
   - Continuer la surveillance

## ⚙️ Configuration

Les paramètres sont enregistrés dans `monitor_config.json`:
- Coordonnées de la région sélectionnée
- Position de clic
- Intervalle de vérification
- Durée de déclenchement
- Seuil de similitude
- Paramètre de mémorisation de position
- Message personnalisé

## 💡 Conseils et Bonnes Pratiques

### Sélection de Région
- Sélectionnez la zone de sortie principale de Claude Code
- Évitez les zones avec curseurs clignotants ou horodatages
- La région doit être assez grande (au moins 100x100 pixels)

### Ajustement des Paramètres
- **Trop sensible?** → Augmentez le seuil à 0.99 ou augmentez le temps de déclenchement
- **Ne se déclenche pas?** → Diminuez le seuil à 0.95 ou réduisez le temps de déclenchement
- **Pour les tâches longues** → Réglez le temps de déclenchement à 60-90 secondes
- **Pour les réponses rapides** → Réglez le temps de déclenchement à 30-45 secondes

## 🛠️ Stack Technique

- **Python 3.7+**
- **tkinter** - Framework GUI
- **pyautogui** - Capture d'écran et automatisation
- **opencv-python** - Comparaison d'images
- **Pillow** - Traitement d'images
- **pyperclip** - Opérations de presse-papiers
- **pywin32** - API Windows
- **PyInstaller** - Empaquetage EXE

## 🐛 Dépannage

### Problème: Le programme ne trouve pas la fenêtre Claude Code
**Solution**: Assurez-vous que la fenêtre est ouverte et visible, non minimisée.

### Problème: L'automatisation ne fonctionne pas
**Solution**:
- Ne déplacez pas la souris vers les coins de l'écran (fonctionnalité de sécurité PyAutoGUI)
- Exécutez en tant qu'administrateur si nécessaire
- Assurez-vous qu'aucune autre fenêtre ne couvre Claude Code

### Problème: Se déclenche toujours (faux positifs)
**Solution**:
- Augmentez le temps de déclenchement
- Augmentez le seuil de similitude (0.99)
- Resélectionnez la région sans éléments dynamiques

### Problème: Ne se déclenche jamais (faux négatifs)
**Solution**:
- Diminuez le seuil (0.95)
- Vérifiez si la région est correctement sélectionnée
- Vérifiez que la surveillance est en cours d'exécution (vérifiez le statut)

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à soumettre une Pull Request.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## ⚠️ Avertissement

Cet outil est destiné à un usage personnel uniquement pour améliorer la productivité. Utilisez-le de manière responsable et conformément à toutes les conditions d'utilisation applicables.

---

Fait avec ❤️ pour la communauté Claude Code
