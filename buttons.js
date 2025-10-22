const display = document.getElementById("display");

document.querySelectorAll(".btn").forEach(button => {
    button.addEventListener("click", () => {
        const action = button.dataset.action;
        handleButton(action);
    });
});