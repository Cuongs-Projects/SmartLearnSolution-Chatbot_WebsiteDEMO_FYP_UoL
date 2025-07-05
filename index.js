
const session = require('express-session');
const express = require('express');
const app = express();
const port = 3000;
const methodOverride = require('method-override');


// in index.js file, i was missing the crucial piece of middleware needed to understand and parse this JSON data.
// with bodyParser, ive been parsing html instead
app.use(express.json()); 
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs'); // set the app to use ejs for rendering
app.use(express.static(__dirname + '/public')); // set location of static files

app.use('/scripts',express.static(__dirname+'/node_modules/showdown/dist/'));
//to access showdown markdown-to-html format converter

//Placing properties inside the session configuration object does not add them to every req.session object. 
// It's just configuration for the session middleware itself. req.session is empty for each new user until you 
// explicitly add properties to it.
app.locals.PYTHON_API_URL = 'http://localhost:5001/generate';
app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: true,
    cookie:{
        //technically set as false, since the website is running on local host and not HTTPS
        //therefore, cookie or any necessary details to be saved would not be saved if I set 'secure' as true
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24 * 7
    },
    // PYTHON_API_URL: 'http://localhost:5001/generate',
    //userID: "abc123" //since no login system, this will do
}));
app.use(methodOverride('_method'));

// Handle requests to the main home page 
app.get('/', (req, res) => {
    res.redirect("/my-courses");
});

app.get('/my-courses', (req, res) => {
    res.render('mainHome.ejs');
});

const showCoursesRoute = require('./routes/show.js');
app.use('/show', showCoursesRoute);

// Make the web application listen for HTTP requests
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})
