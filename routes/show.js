const express = require("express");
const router = express.Router();
// const sanitizeHtml = require('sanitize-html');
// const sanitizedOptions = {
//     allowedTags: [], //allows no html tags
//     allowedAttributes: {} //allows no attributes
// };

const axios = require('axios');

const course_dict = {
    2:"PADBRC",
    12:"PF30DRPP"
}
const course_name_dict = {
    "PADBRC":"Program A - Developing basic research capacities - 30 - Day DTR",
    "PF30DRPP":"Program F - 30 - day research publication preparation"
}
const course_instructors_dict = {
    "PADBRC":"Dr. Ngô Mai and Dr. Nghĩa Trần",
    "PF30DRPP":"Dr. Ngô Mai and Dr. Nghĩa Trần"
}
const saveFullResponse = require('../public/js/saveConvo.js');
const loadFullResponse = require('../public/js/retrieveConvo.js');

function isLoggedIn(req, res, next){
    if (!req.session.userID) {
        req.session.redirectTo = req.originalUrl;
        res.redirect("/login");
    }else{
        next();
    }
}

router.get("/coursecontent/:courseID",isLoggedIn,(req, res, next) => {
    const userID = req.session.userID;
    const courseID= req.params.courseID;
    const courseName = course_dict[courseID]
    if (!req.session.prompt_type || courseName != req.session.current_courseName) {
        req.session.prompt_type = 'init'
    }
    req.session.current_courseName = courseName
    const full_response = loadFullResponse(userID,courseName);
    if (full_response != null && full_response.length > 1) {
        req.session.prompt_type = 'cont'
    }
    res.render("courses/course_page.ejs", {name: courseName, user: userID});
});

router.post("/ask",isLoggedIn, async (req, res) => {
    //receives the 'body' sent by the fetch call.
    const userQuestion = req.body.question;
    const courseIdentifier = req.session.current_courseName;
    const full_response = req.body.full_response;
    const prompt_type = req.body.prompt_type;
    const module_name = course_name_dict[courseIdentifier];
    const instructors = course_instructors_dict[courseIdentifier];

    //communicatewith the Python API.
    const response = await axios.post(req.app.locals.PYTHON_API_URL, {
        question: userQuestion,
        collection_name: `smartlearn_${courseIdentifier.toLowerCase()}`,
        full_response: full_response,
        prompt_type: prompt_type,
        module_name: module_name,
        instructors: instructors
    });

    //sends the answer back to the original sender (the browser's fetch call).
    res.json({ answer: response.data.answer, 
               prompt_type: response.data.prompt_type, 
               full_response: response.data.full_response});
});

router.get('/conversation-get',isLoggedIn, (req, res) => {
    const userID = req.session.userID;
    const courseName = req.session.current_courseName;
    let full_response = loadFullResponse(userID,courseName);
    if (full_response == null) {
        full_response = ""
    }
    res.json({ full_response: full_response, prompt_type: req.session.prompt_type});
});

router.post('/conversation-save',isLoggedIn, (req, res) => {
    const userID = req.session.userID;
    const courseName = req.session.current_courseName;
    const full_response = req.body.full_response;
    const prompt_type = req.body.prompt_type;
    req.session.prompt_type = prompt_type
    saveFullResponse(userID,courseName,full_response);
    res.json({ status: 'saved' });
});

module.exports = router;