const bodyParser = require('body-parser');
const express = require('express');
const app = express();
const path = require('path')

app.use(require('./routes/index'));

app.use(express.static(path.join(__dirname,'/html/index.html')));
app.use(express.urlencoded({ extended: false}));




// main route
 app.get('/', (req,res) => {
    //home page
    res.sendFile(path.join(__dirname, "/html/index.html"))
});

//download pdf cv
// var cv = express().descargar(function () {
//     this.use('/assets',express.static('assets'));
// });

app.listen(3000, ()=>{
    console.log('Server on port 3000')
});

module.exports = app;