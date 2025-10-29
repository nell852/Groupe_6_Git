// Exécute le code uniquement après que le DOM soit complètement chargé
document.addEventListener("DOMContentLoaded", () => {
    const historyDiv = document.getElementById("history");

    if (!historyDiv) {
        console.warn("⚠️ L'élément #history est introuvable dans le DOM.");
        return; // On sort proprement, rien à faire
    }

    // --- Fonction pour ajouter une entrée dans l’historique ---
    function addToHistory(entry {
        if (!entry) return; // Évite les lignes vides

        const line = document.createElement("div");
        line.classList.add("history-item");
        line.textContent = entry;

        // Ajoute l’entrée en haut avec une petite animation
        historyDiv.prepend(line);

        // Limite le nombre d’éléments à 10 maximum
        const maxItems = 10;
        const items = historyDiv.querySelectorAll(".history-item");
        if (items.length > maxItems) {
            historyDiv.removeChild(items[items.length - 1]);
        }
    }

    // --- Exemple d'utilisation pour test ---
    // addToHistory("Historique initialisé avec succès !");
    
    // Tu peux appeler `addToHistory("texte")` depuis un autre script
    window.addToHistory = addToHistory;
});
