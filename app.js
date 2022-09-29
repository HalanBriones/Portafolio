const bodyParser = require('body-parser');
const express = require('express');

const http = require('http');

const app = express();
const path = require('path')
const PORT = 80

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

app.get('/', (req,res) => {
    //home page
    res.sendFile(path.join(__dirname, "/html/index.html"))
    // res.send('this is the home page');
});

app.get('/views/projects', (req,res) =>{
    // res.sendFile(path.join(__dirname, "views/index.html"))
    // res.send('this is projects page');
});

const port = parseInt(process.env,PORT,10) || 80;
app.set('port',port);

const server = http.createServer(app);
server.listen(port);

module.exports = app;