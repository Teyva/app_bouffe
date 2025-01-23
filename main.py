import json
import hashlib
from tkinter import messagebox, simpledialog
import os
import tkinter as tk

# Fichiers JSON
FICHIER_UTILISATEURS = "utilisateurs.json"
FICHIER_PRODUITS = "produits.json"

# Charger un fichier JSON
def charger_json(fichier, structure_initiale):
    if not os.path.exists(fichier):
        with open(fichier, "w") as f:
            json.dump(structure_initiale, f, indent=4)
    with open(fichier, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            with open(fichier, "w") as f:
                json.dump(structure_initiale, f, indent=4)
            return structure_initiale

# Sauvegarder un fichier JSON
def sauvegarder_json(fichier, contenu):
    with open(fichier, "w") as f:
        json.dump(contenu, f, indent=4)

# Initialiser les fichiers avec un compte administrateur par défaut
def initialiser_utilisateurs():
    utilisateurs = charger_json(FICHIER_UTILISATEURS, {"utilisateurs": []})
    if not any(user["username"] == "admin" for user in utilisateurs["utilisateurs"]):
        utilisateurs["utilisateurs"].append({
            "username": "admin",
            "password": hasher_mot_de_passe("admin"),
            "role": "admin",
            "solde": 0.0
        })
        sauvegarder_json(FICHIER_UTILISATEURS, utilisateurs)

# Hash du mot de passe
def hasher_mot_de_passe(password):
    return hashlib.md5(password.encode()).hexdigest()

# Connexion utilisateur
def connexion(utilisateurs, username, password):
    for user in utilisateurs["utilisateurs"]:
        if user["username"] == username and user["password"] == hasher_mot_de_passe(password):
            return user
    return None

# Application principale
def application_principale():
    root = tk.Tk()
    root.title("Application de Gestion")
    root.geometry("900x650")
    root.configure(bg="#f0f0f0")

    utilisateurs = charger_json(FICHIER_UTILISATEURS, {"utilisateurs": []})
    produits = charger_json(FICHIER_PRODUITS, {"produits": []})

    # Conteneur principal
    container = tk.Frame(root, bg="#f0f0f0")
    container.pack(fill="both", expand=True)

    # Dictionnaire des cadres
    frames = {}

    # Changer de cadre
    def afficher_cadre(nom_cadre):
        frame = frames[nom_cadre]
        frame.tkraise()
        if nom_cadre == "ConnexionFrame":
            frames["ConnexionFrame"].reset_fields()

# Connexion utilisateur (mis à jour avec champs séparés pour création de compte)
    class ConnexionFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, bg="#f0f0f0")
            tk.Label(self, text="Connexion", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)

            # Champs de connexion
            tk.Label(self, text="Nom d'utilisateur :", bg="#f0f0f0").pack(pady=5)
            self.entry_username = tk.Entry(self, width=30)
            self.entry_username.pack(pady=5)

            tk.Label(self, text="Mot de passe :", bg="#f0f0f0").pack(pady=5)
            self.entry_password = tk.Entry(self, width=30, show="*")
            self.entry_password.pack(pady=5)

            btn_connexion = tk.Button(self, text="Se connecter", command=self.connexion_ui, bg="#4caf50", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_connexion.pack(pady=10)

            # Bouton pour afficher les champs de création de compte
            btn_creer_compte = tk.Button(self, text="Créer un compte", command=self.afficher_champs_creation, bg="#2196f3", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_creer_compte.pack(pady=10)

            # Champs de création de compte (initialement cachés)
            self.cadre_creation = tk.Frame(self, bg="#f0f0f0")

            tk.Label(self.cadre_creation, text="Nom d'utilisateur (nouveau) :", bg="#f0f0f0").pack(pady=5)
            self.entry_new_username = tk.Entry(self.cadre_creation, width=30)
            self.entry_new_username.pack(pady=5)

            tk.Label(self.cadre_creation, text="Mot de passe (nouveau) :", bg="#f0f0f0").pack(pady=5)
            self.entry_new_password = tk.Entry(self.cadre_creation, width=30, show="*")
            self.entry_new_password.pack(pady=5)

            btn_valider_creation = tk.Button(
                self.cadre_creation, text="Valider", command=self.creer_compte_ui, bg="#4caf50", fg="white", width=20, font=("Helvetica", 10, "bold")
            )
            btn_valider_creation.pack(pady=10)

        def connexion_ui(self):
            username = self.entry_username.get()
            password = self.entry_password.get()
            if username and password:
                user = connexion(utilisateurs, username, password)
                if user:
                    if user["role"] == "admin":
                        afficher_cadre("AdminFrame")
                    elif user["role"] == "client":
                        frames["ClientFrame"].set_user(user)
                        afficher_cadre("ClientFrame")
                else:
                    messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        def afficher_champs_creation(self):
            self.cadre_creation.pack(pady=10)

        def creer_compte_ui(self):
            username = self.entry_new_username.get()
            password = self.entry_new_password.get()

            if not username or not password:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs pour créer un compte.")
                return

            if any(user["username"] == username for user in utilisateurs["utilisateurs"]):
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
                return

            utilisateurs["utilisateurs"].append({
                "username": username,
                "password": hasher_mot_de_passe(password),
                "role": "client",
                "solde": 0.0
            })
            sauvegarder_json(FICHIER_UTILISATEURS, utilisateurs)
            messagebox.showinfo("Succès", "Compte créé avec succès ! Vous êtes maintenant connecté.")

            # Connecter automatiquement l'utilisateur après la création du compte
            user = connexion(utilisateurs, username, password)
            if user:
                frames["ClientFrame"].set_user(user)
                afficher_cadre("ClientFrame")

        def reset_fields(self):
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            if hasattr(self, 'entry_new_username'):
                self.entry_new_username.delete(0, tk.END)
            if hasattr(self, 'entry_new_password'):
                self.entry_new_password.delete(0, tk.END)


    # Interface Client
    class ClientFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, bg="#f0f0f0")
            self.user = None
            tk.Label(self, text="Espace Client", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)
            
            self.label_solde = tk.Label(self, font=("Helvetica", 14), bg="#f0f0f0")
            self.label_solde.pack(pady=10)

            self.cadre_produits = tk.Frame(self, bg="#f0f0f0")
            self.cadre_produits.pack(pady=10)

            btn_payer = tk.Button(self, text="Payer un montant", command=self.payer_montant, bg="#4caf50", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_payer.pack(pady=10)

            btn_retour = tk.Button(self, text="Déconnexion", command=lambda: afficher_cadre("ConnexionFrame"), bg="#f44336", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_retour.pack(pady=20)

        def set_user(self, user):
            self.user = user
            self.mettre_a_jour_interface()

        def payer_montant(self):
            montant = simpledialog.askfloat("Paiement", "Entrez le montant que vous voulez payer :")
            if montant is not None and montant > 0:
                self.user["solde"] += montant
                sauvegarder_json(FICHIER_UTILISATEURS, utilisateurs)
                self.mettre_a_jour_interface()
            elif montant is not None:
                messagebox.showerror("Erreur", "Le montant doit être positif.")

        def mettre_a_jour_interface(self):
            self.label_solde.config(text=f"Solde : {self.user['solde']:.2f}$")
            for widget in self.cadre_produits.winfo_children():
                widget.destroy()
            for produit in produits["produits"]:
                btn = tk.Button(
                    self.cadre_produits,
                    text=f"{produit['nom']} - {produit['prix']}$ (Stock : {produit['quantite']})",
                    command=lambda p=produit: self.acheter_produit(p),
                    width=40,
                    height=2,
                    bg="#bbdefb",
                    font=("Helvetica", 10)
                )
                btn.pack(pady=5)

        def acheter_produit(self, produit):
            if produit["quantite"] > 0 :
                produit["quantite"] -= 1
                self.user["solde"] -= produit["prix"]
                sauvegarder_json(FICHIER_PRODUITS, produits)
                sauvegarder_json(FICHIER_UTILISATEURS, utilisateurs)
                self.mettre_a_jour_interface()
            elif produit["quantite"] <= 0:
                messagebox.showerror("Rupture de stock", "Ce produit est en rupture de stock.")

    # Interface Administrateur
    class AdminFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, bg="#f0f0f0")
            tk.Label(self, text="Espace Administrateur", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)
            
            btn_gestion_produits = tk.Button(self, text="Gestion des Produits", command=lambda: afficher_cadre("GestionProduitsFrame"), bg="#2196f3", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_gestion_produits.pack(pady=20)

            btn_gestion_utilisateurs = tk.Button(self, text="Gestion des Utilisateurs", command=lambda: afficher_cadre("GestionUtilisateursFrame"), bg="#4caf50", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_gestion_utilisateurs.pack(pady=20)

            btn_retour = tk.Button(self, text="Déconnexion", command=lambda: afficher_cadre("ConnexionFrame"), bg="#f44336", fg="white", width=20, font=("Helvetica", 10, "bold"))
            btn_retour.pack(pady=20)

    # Interface Gestion des Produits
    class GestionProduitsFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, bg="#f0f0f0")
            self.produits = produits
            tk.Label(self, text="Gestion des Produits", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)

            # Cadre pour la liste des produits
            self.cadre_produits = tk.Frame(self, bg="#f0f0f0")
            self.cadre_produits.pack(pady=20)

            # Section pour ajouter un produit
            cadre_ajout = tk.Frame(self, bg="#f0f0f0")
            cadre_ajout.pack(pady=20)

            tk.Label(cadre_ajout, text="Nom :", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
            self.entry_nom = tk.Entry(cadre_ajout, width=20)
            self.entry_nom.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(cadre_ajout, text="Prix :", bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=5)
            self.entry_prix = tk.Entry(cadre_ajout, width=10)
            self.entry_prix.grid(row=0, column=3, padx=10, pady=5)

            tk.Label(cadre_ajout, text="Quantité :", bg="#f0f0f0").grid(row=0, column=4, padx=10, pady=5)
            self.entry_quantite = tk.Entry(cadre_ajout, width=10)
            self.entry_quantite.grid(row=0, column=5, padx=10, pady=5)

            btn_ajouter = tk.Button(
                cadre_ajout,
                text="Ajouter le produit",
                command=self.ajouter_produit,
                bg="#4caf50",
                fg="white",
                font=("Helvetica", 10, "bold"),
            )
            btn_ajouter.grid(row=0, column=6, padx=10, pady=5)

            # Bouton retour
            btn_retour = tk.Button(self, text="Retour", command=lambda: afficher_cadre("AdminFrame"), bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
            btn_retour.pack(pady=20)

            self.mettre_a_jour_interface()

        def ajouter_produit(self):
            """Ajouter un produit à partir des champs."""
            nom = self.entry_nom.get().strip()
            try:
                prix = float(self.entry_prix.get().strip())
                stock = int(self.entry_quantite.get().strip())

                if nom and prix > 0 and stock >= 0:
                    self.produits["produits"].append({"nom": nom, "prix": prix, "quantite": stock})
                    sauvegarder_json(FICHIER_PRODUITS, self.produits)
                    self.mettre_a_jour_interface()
                    self.entry_nom.delete(0, tk.END)
                    self.entry_prix.delete(0, tk.END)
                    self.entry_quantite.delete(0, tk.END)
                else:
                    messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour le nom, le prix et la quantité.")
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour le prix et la quantité.")

        def mettre_a_jour_interface(self):
            """Met à jour la liste des produits affichée à l'écran."""
            for widget in self.cadre_produits.winfo_children():
                widget.destroy()

            for produit in self.produits["produits"]:
                row = self.produits["produits"].index(produit)

                tk.Label(self.cadre_produits, text=f"{produit['nom']} (Stock: {produit['quantite']}, Prix: {produit['prix']}$)", bg="#f0f0f0", font=("Helvetica", 10)).grid(row=row, column=0, padx=10, pady=5)

                entry_stock = tk.Entry(self.cadre_produits, width=10)
                entry_stock.insert(0, produit["quantite"])
                entry_stock.grid(row=row, column=1, padx=10, pady=5)

                entry_prix = tk.Entry(self.cadre_produits, width=10)
                entry_prix.insert(0, produit["prix"])
                entry_prix.grid(row=row, column=2, padx=10, pady=5)

                btn_valider = tk.Button(
                    self.cadre_produits,
                    text="Valider",
                    command=lambda p=produit, es=entry_stock, ep=entry_prix: self.modifier_produit(p, es, ep),
                    bg="#4caf50", fg="white", font=("Helvetica", 8))
                btn_valider.grid(row=row, column=3, padx=10, pady=5)

                btn_supprimer = tk.Button(
                    self.cadre_produits,
                    text="Supprimer",
                    command=lambda p=produit: self.retirer_produit(p),
                    bg="#f44336", fg="white", font=("Helvetica", 8))
                btn_supprimer.grid(row=row, column=4, padx=10, pady=5)

        def modifier_produit(self, produit, entry_stock, entry_prix):
            try:
                produit["quantite"] = int(entry_stock.get())
                produit["prix"] = float(entry_prix.get())
                sauvegarder_json(FICHIER_PRODUITS, self.produits)
                self.mettre_a_jour_interface()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour le stock et le prix.")

        def retirer_produit(self, produit):
            self.produits["produits"].remove(produit)
            sauvegarder_json(FICHIER_PRODUITS, self.produits)
            messagebox.showinfo("Succès", f"Produit '{produit['nom']}' supprimé avec succès.")
            self.mettre_a_jour_interface()

    # Interface Gestion des Utilisateurs
    class GestionUtilisateursFrame(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent, bg="#f0f0f0")
            self.utilisateurs = utilisateurs
            tk.Label(self, text="Gestion des Utilisateurs", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=20)

            self.cadre_utilisateurs = tk.Frame(self, bg="#f0f0f0")
            self.cadre_utilisateurs.pack(pady=20)

            btn_retour = tk.Button(self, text="Retour", command=lambda: afficher_cadre("AdminFrame"), bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
            btn_retour.pack(pady=20)

            self.mettre_a_jour_interface()

        def mettre_a_jour_interface(self):
            for widget in self.cadre_utilisateurs.winfo_children():
                widget.destroy()
            for utilisateur in self.utilisateurs["utilisateurs"]:
                row = self.utilisateurs["utilisateurs"].index(utilisateur)
                label_user = tk.Label(self.cadre_utilisateurs, text=f"{utilisateur['username']} (Rôle: {utilisateur['role']}, Solde: {utilisateur['solde']:.2f}€)", bg="#f0f0f0", font=("Helvetica", 10))
                label_user.grid(row=row, column=0, padx=10, pady=5)

                entry_solde = tk.Entry(self.cadre_utilisateurs, width=10)
                entry_solde.insert(0, utilisateur["solde"])
                entry_solde.grid(row=row, column=1, padx=10, pady=5)

                btn_valider = tk.Button(self.cadre_utilisateurs, text="Valider", command=lambda u=utilisateur, e=entry_solde: self.modifier_solde(u, e), bg="#4caf50", fg="white", font=("Helvetica", 8))
                btn_valider.grid(row=row, column=2, padx=10, pady=5)

        def modifier_solde(self, utilisateur, entry):
            try:
                utilisateur["solde"] = float(entry.get())
                sauvegarder_json(FICHIER_UTILISATEURS, self.utilisateurs)
                messagebox.showinfo("Succès", f"Solde de {utilisateur['username']} mis à jour avec succès.")
                self.mettre_a_jour_interface()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une valeur valide.")

    # Créer les cadres
    frames["ConnexionFrame"] = ConnexionFrame(container)
    frames["ClientFrame"] = ClientFrame(container)
    frames["AdminFrame"] = AdminFrame(container)
    frames["GestionProduitsFrame"] = GestionProduitsFrame(container)
    frames["GestionUtilisateursFrame"] = GestionUtilisateursFrame(container)

    for frame in frames.values():
        frame.place(relwidth=1, relheight=1)

    afficher_cadre("ConnexionFrame")
    root.mainloop()
# Exécuter l'application
if __name__ == "__main__":
    initialiser_utilisateurs()
    application_principale()
