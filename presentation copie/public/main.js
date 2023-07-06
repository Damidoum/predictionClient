// data.js
// Contient les fonctions pour manipuler les données

function changeClient() {
    var selectedClient = document.getElementById("client-select").value;
    var clientContent = document.getElementById("client-content");

    // Vider le contenu précédent du client
    clientContent.innerHTML = "";

    if (selectedClient === "") {
        // Si aucun client n'est sélectionné, afficher un message
        clientContent.innerHTML = "<p>Veuillez sélectionner un client.</p>";
    } else if (selectedClient == "global-results") {
        let template = generateResultTemplate();
        clientContent.innerHTML = template;
    } else {
        // Afficher les informations du client sélectionné
        //displayData(selectedClient);
        var template = generateClientTemplate();
        clientContent.innerHTML = template;
        displayData(selectedClient);
    }
}

function generateClientTemplate() {
    return `
    <div class="global-chart-container">
    <div class=first-chart-container>
        <div class="presentation">
            <h1>Présentation des données</h1>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart0"></canvas>
        </div>
    </div>
    <div class="corr">
        <h3>Etude des corrélations</h3>
        <div class="images-container">
            <img class="client-image" id="image0">
        </div>
        <div class="images-container">
            <img class="client-image" id="image1">
        </div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Premier modèle : Régression linéaire</h1>
            <p> Régression linéaire effectuée sur la seule variable disponible : la prédiction du client.</p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart1"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter1"></canvas>
        </div>
        <div id=error1></div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Deuxième modèle : Régression linéaire</h1>
            <p> Régression linéaire effectuée sur la variable de prédiction client mais aussi sur des variables
                ajoutés
                après étude des données qu'on avait à disposition en open source (météo, bourse).</p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart2"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter2"></canvas>
        </div>
        <div id=error2></div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Troisième modèle : Random Forest</h1>
            <p>On a cette fois-ci gardé toutes les données que nous avions trouvé. Nous avons simplement changé
                le
                modèle,
                nous utilisons cette fois-ci un modèle de fôrets aléatoires.
            </p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart3"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter3"></canvas>
        </div>
        <div id=error3></div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Quatrième modèle : Gradient Boosting</h1>
            <p>Cette fois-ci c'est un modèle de Boosting qui est utilisé.
            </p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart4"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter4"></canvas>
        </div>
        <div id=error4></div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Cinquième modèle : Support Vector Machine </h1>
            <p>Le Support Vector Machine est modèle qui utilise un noyau. Nous avons utiliser un noyau
                polynomiale
                d'ordre
                quatre. Ce choix a été fait par validation croisée.
            </p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart5"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter5"></canvas>
        </div>
        <div id=error5></div>
    </div>

    <div class=chart>
        <div class="presentation">
            <h1>Sixième modèle : Random Forest en prenant en compte le biais </h1>
            <p>Ajout d'un bruit gaussien pour perturber les données boursières. Cela permet de faire comme si ces
                données étaient prédites deux semaines à l'avance
            </p>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="chart6"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title"></div>
            <canvas id="scatter6"></canvas>
        </div>
        <div id=error6></div>
    </div>

    <div class=results>
        <h1> Synthèses des différents modèles </h1>
        <div class="results-container">
            <canvas id="chart-results-mse"></canvas>
        </div>
        <div class="results-container">
            <canvas id="chart-results-mae"></canvas>
        </div>
        <div class="results-container">
            <canvas id="chart-results-r2"></canvas>
        </div>
        <div class="results-container">
            <canvas id="chart-results"></canvas>
        </div>
    </div>
</div>    `;
}



function generateResultTemplate() {
    return ``
}