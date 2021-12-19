var playing = false;
var score;
var correctAnswer;

document.getElementById("startreset").onclick = () => {
    if (playing == true) {
        location.reload(true);
    } else {
        playing = true
        score = 0;
        remainingTime();
        show("timeremaining");
        hide("gameOver");
        hide("logout")
        text("startreset", "Reset Game");
        generateQA();
    }
}

document.getElementById("logout").onclick = () => {
    playing;
}

for (let i = 1; i < 5; i++) {
    document.getElementById("box"+i).onclick = () => {
        if (playing == true) {
            if (document.getElementById("box"+i).innerHTML == correctAnswer) {
                score++;

                document.getElementById("scorevalue").innerHTML = score;

                hide("wrong");
                show("correct");
                setTimeout(() => {
                    hide("correct");
                }, 1000);
                
                generateQA();
            }else{
                hide("correct");
                show("wrong");
                setTimeout(() => {
                    hide("wrong");
                }, 1000);
            }
        }
    }
}

var remainingTime = () => {
    var time = 31;
    setInterval(() => {
        time--;
        if (time >= 0) {
            // ACTIVE TIME
            document.getElementById("timeremainingvalue").innerHTML = " " + time + " ";
        } else {
            // expired time
            clearInterval(this);
            document.getElementById("gameOver").innerHTML = "<p>Game Over</p><p>Your score is: " + score + "</p>";
            show("gameOver");
            show("logout")
            hide("timeremaining");
        }
    }, 1000);
}

var generateQA = () => {
    var x = Math.floor(Math.random() * 9) + 1;
    var y = Math.floor(Math.random() * 9) + 1;
    correctAnswer = x * y;
    var correctPosition = 1 + (Math.round(3 * Math.random()));

    var answers = [correctAnswer];

    // console.log(x, y);
    // console.log(correctPosition);
    // console.log(correctAnswer)

    // displaying question 
    document.getElementById("question").innerHTML = "<p>" + x + " X " + y + "</p>";

    for (let i = 1; i <= 4; i++) {
        if (i != correctAnswer) {
            do {
                // generate random wrong answer
                var wrongAnswer = (Math.floor(Math.random() * 9) + 1) * (Math.floor(Math.random() * 9) + 1);
                document.getElementById("box" + i).innerHTML = wrongAnswer;
            } while (answers.indexOf(wrongAnswer) > -1);
        }
    }
    // disaplying correct answer
    document.getElementById("box"+correctPosition).innerHTML = correctAnswer;
    answers.push(wrongAnswer);
    return correctAnswer;
}

// FAST EASY FUNCTIONS
var show = (id) => {
    document.getElementById(id).style.display = "block";
}

var hide = (id) => {
    document.getElementById(id).style.display = "none";
}

var text = (id, text) => {
    document.getElementById(id).innerHTML = text;
}

var showTimeout = (id, time) => {
    setTimeout(() => {
        show(id)
    }, time);
}

show("gameOver");
text("gameOver", "<p>Please click 'start game' to play</p>");
text("startreset", "Start Game");