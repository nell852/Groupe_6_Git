const display = document.getElementById("display");
const buttons = document.querySelectorAll(".btn");

buttons.forEach(btn => {
    btn.addEventListener("click", e => {
        const action = e.target.dataset.action;
        if (!action) return;

        btn.classList.add("active");
        setTimeout(() => btn.classList.remove("active"), 150);

        try {
            handleButton(action);
        } catch (error) {
            console.error("Erreur lors du traitement du bouton :", error);
        }
    });
});
