const express = require('express');
const app = express();

const path = require('path');
const csv = require('csv-parser');
const fs = require('fs');

function parseCSV(filePath, callback) {
    const tabData = [];

    fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (data) => {
            tabData.push(data);
        })
        .on('end', () => {
            console.log(`Données CSV pour le fichier ${filePath} chargées avec succès`);
            callback(tabData);
        });
}


app.get('/data/:client/:file', (req, res) => {
    const client = req.params.client;
    const file = req.params.file;
    const filePath = `../../output/${client}/plot/${file}`;

    parseCSV(filePath, (tabData) => {
        const chartData = tabData.map(entry => ({
            time: entry.time,
            y1: parseFloat(entry.y1),
            y2: parseFloat(entry.y2)
        }));
        res.json(chartData);
    });
});

app.get('/images/:client/:image', (req, res) => {
    const client = req.params.client;
    const image = req.params.image;
    const imagePath = path.resolve(__dirname, `../../output/${client}/${image}`);
    res.sendFile(imagePath);
});

app.get('/results/:client', (req, res) => {
    const client = req.params.client;
    const results = path.resolve(__dirname, `../../output/${client}/results.csv`);

    parseCSV(results, (tabData) => {
        const chartData = tabData.map(entry => ({
            MSE: parseFloat(entry.MSE),
            MAE: parseFloat(entry.MAE),
            R2: parseFloat(entry.R2),
            crossVal: entry.crossVal
        }));
        res.json(chartData);
    });

});

app.get('/global-results/:loss', (req, res) => {
    const loss = req.params.loss;
    const results = path.resolve(__dirname, `../../output/global_results/${loss}`);

    parseCSV(results, (tabData) => {
        const chartData = tabData.map(entry => ({
            clients: parseFloat(entry.id_client),
            modele0: parseFloat(entry.y0),
            modele1: parseFloat(entry.y1),
            modele2: parseFloat(entry.y2),
            modele3: parseFloat(entry.y3),
            modele4: parseFloat(entry.y4),
            modele5: parseFloat(entry.y5),
            modele6: parseFloat(entry.y6),
        }));
        res.json(chartData);
    });

});

// Définition du dossier contenant les fichiers statiques
app.use(express.static(__dirname));

// Route pour renvoyer le fichier index.html
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Écoute du serveur sur le port 3000
app.listen(3000, () => {
    console.log('Le serveur est en cours d\'exécution sur le port 3000');
});
