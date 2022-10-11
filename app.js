const express = require('express');
const app = express();
const path = require('path')
const bodyParser = require('body-parser');
const nodeMailer = require('nodemailer');
const fs = require("fs");
require('dotenv').config();

const puerto = process.env.PORT || 3000;


//app.use(require('./routes/index'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(express.static(path.join(__dirname,'/public')));
app.use(express.static(path.join(__dirname,'/html')));

app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);

app.post('/email', function (req, res) {
    let transporter = nodeMailer.createTransport({
        service: 'gmail',
        auth: {
            user:process.env.EMAIL,
            pass: process.env.PASSWORD
        }
    });

    let mailOptions = {
        from: process.env.EMAIL, // sender address desde donde se enviara el email
        to:'halanbm98@gmail.com', // list of receivers la persona que quiere que lo contactes
        subject: req.body.subject, // Subject line objetivo de la solicitud de contacto
        text: req.body.message, // plain text body Mensage 
        html: '<b>' + req.body.name + ' esta solicitando que lo contactes a su correo que es '+ req.body.email+ '<br>' +' Mensaje adjuntado dice: '+ req.body.message +'</b>' // html body
    };
    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            return console.log(error);
        }else{
            res.status(201).render(path.join(__dirname, "/html/index.html"));
        }
    });
    // res.sendFile(path.join(__dirname, "/html/index.html"))
    
});

// main route
 app.get('/', (req,res) => {
    //home page
    res.sendFile(path.join(__dirname, "/html/index.html", isAdded = false))
});

app.get('/pdf', function (req, res) {
    var filePath = "/public/assets/docs/CV-Halan-Briones-IT.pdf";

    fs.readFile(__dirname + filePath , function (err,data){
        res.contentType("application/pdf");
        res.send(data);
    });
});


app.listen(puerto, ()=>{
    console.log('Server on port: ' + puerto)
});

module.exports = app;