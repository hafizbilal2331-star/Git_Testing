document.addEventListener("DOMContentLoaded", function () {
    console.log("Patients JS loaded");
    document.querySelectorAll(".patient-item").forEach(item => {
        item.addEventListener("click", () => {
            item.style.backgroundColor = "";
        });
    });
});
