const session = require('express-session');
const express = require('express');
const app = express();
const port = 3000;
const methodOverride = require('method-override');
// var bodyParser = require("body-parser");
const sanitizeHtml = require('sanitize-html');
const sanitizedOptions = {
    allowedTags: [],
    allowedAttributes: {}
};


app.use(express.json()); 
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs'); 
app.use(express.static(__dirname + '/public')); 

app.use('/scripts',express.static(__dirname+'/node_modules/showdown/dist/'));

app.locals.PYTHON_API_URL = 'http://localhost:5001/generate';
app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: true,
    cookie:{
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24 * 7
    },
}));
app.use(methodOverride('_method'));


function isLoggedIn(req, res, next){
    if (!req.session.userID) {
        req.session.redirectTo = req.originalUrl;
        res.redirect("/login");
    }else{
        next();
    }
}

app.get("/login", (req, res, next) => {
    res.render("student/login.ejs");
});

//to handle the login process
//an extremely simple hard coded login for demo
app.post("/logging_in",(req, res, next) => {
    const presanitizedusername = req.body.username;
    const presanitizedpassword = req.body.password;
    const username = sanitizeHtml(presanitizedusername, sanitizedOptions);
    const password = sanitizeHtml(presanitizedpassword, sanitizedOptions);
    //The user's password would be encrypted and stored in a database.
    // The proper implementation would be retrieving the encrypted text, 
        // decrypt, compare, and provide the userID for the chatbot 
    if (username == "admin" && password == "admin"){
        req.session.userID = 'abc123'
        const redirectTo = req.session.redirectTo || "/";
        res.redirect(redirectTo)
    }else{
        let script = `<script>alert("Incorrect password"); window.history.back();</script>`;
        res.send(script);
    }
});

app.get('/',(req, res) => {
    res.redirect("/my-courses");
});

app.get('/my-courses',isLoggedIn,(req, res) => {
    res.render('mainHome.ejs');
});


const showCoursesRoute = require('./routes/show.js');
app.use('/show', showCoursesRoute);

// Make the web application listen for HTTP requests
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})
