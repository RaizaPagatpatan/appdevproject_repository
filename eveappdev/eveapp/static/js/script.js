const menu = document.querySelector(".ic-menu")
const nav = document.querySelector(".box-ul-nav")

menu.addEventListener('click', () => {
    nav.classList.toggle("active")
})


function openErrorPopup() {
    var errorPopup = document.getElementById("errorPopup");
    errorPopup.style.display = "block";
}

function closeErrorPopup() {
    var errorPopup = document.getElementById("errorPopup");
    errorPopup.style.display = "none";
}

window.onload = function() {
    if ("{{ error_message }}" !== "") {
        openErrorPopup();
    }
};