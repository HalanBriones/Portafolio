const {Router} = require('express');
const { path } = require('../app');
const router = Router();


router.post('/email', (req,res) => {
    console.log('email');
    res.send(req.body);
    
})



module.exports = router;