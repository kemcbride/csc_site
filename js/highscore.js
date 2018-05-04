relevant_divs = document.getElementsByClassName('itg');
console.log(relevant_divs);
hss = scores['highscores'];

// I know that the scores are in a list object called 'scores'
for (i = 0; i < hss.length; i++) {
    console.log(i);
    console.log(relevant_divs[i]);
}
