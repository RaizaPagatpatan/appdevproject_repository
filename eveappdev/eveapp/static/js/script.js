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