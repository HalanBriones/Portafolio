const bodyParser = require('body-parser');
const express = require('express');

const http = require('http');

const app = express();
const path = require('path')
const PORT = 80

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

// main route
app.get('/', (req,res) => {
    //home page
    res.sendFile(path.join(__dirname, "/html/index.html"))
    // res.send('this is the home page');
});

//download pdf cv

var cv = express().descargar(function () {
    this.use('/assets',express.static('assets'));
});

const port = parseInt(process.env,PORT,10) || 80;
app.set('port',port);

const server = http.createServer(app);
server.listen(port);

module.exports = app;