const express = require('express');
const app = express();
const path = require('path')
const bodyParser = require('body-parser');
const nodeMailer = require('nodemailer');

//app.use(require('./routes/index'));

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname,'/html/index.html')));

app.post('/email', function (req, res) {
let transporter = nodeMailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'halanbrionesmerino@gmail.com',
        pass: 'rmedbksgcdvunggr'
    }
});

let mailOptions = {
    from: 'halanbrionesmerino@gmail.com', // sender address desde donde se enviara el email
    to: 'halanbm98@gmail.com', // list of receivers la persona que quiere que lo contactes
    subject: req.body.subject, // Subject line objetivo de la solicitud de contacto
    text: req.body.message, // plain text body Mensage 
    html: '<b>' + req.body.name + ' esta solicitando que lo contactes a su correo que es '+ req.body.email +' Mensaje adjuntado dice: '+ req.body.message +'</b>' // html body
};
transporter.sendMail(mailOptions, (error, info) => {
if (error) {
    return console.log(error);
}else{
    window.alert('Sent Succesfull')
    res.sendFile(path.join(__dirname,"/html/index.html"));
}
});
});

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