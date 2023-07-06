function toggleFullscreen(element) {
    if (!document.fullscreenElement) {
        // Passer en mode plein écran
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) { // Firefox
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) { // Chrome, Safari and Opera
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) { // IE/Edge
            element.msRequestFullscreen();
        }

        // Sauvegarder la taille d'origine du graphique
        element.dataset.originalWidth = element.offsetWidth;
        element.dataset.originalHeight = element.offsetHeight;

        // Ajuster la taille du graphique pour remplir l'écran
        element.style.width = "100%";
        element.style.height = "100%";
    } else {
        // Quitter le mode plein écran
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
            document.msExitFullscreen();
        }

        // Restaurer la taille d'origine du graphique
        element.style.width = element.dataset.originalWidth;
        element.style.height = element.dataset.originalHeight;

        // Supprimer les données sauvegardées
        delete element.dataset.originalWidth;
        delete element.dataset.originalHeight;
    }
}

function parseListFloat(list) {
    let floatList = list.replace(/\[\s+/, '[').replace(/\s+/g, ' ').replace(/\s+\]/, ']').slice(1, -1).split(" ").map(parseFloat);
    return floatList;
}
