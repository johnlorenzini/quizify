async function convert_data(event){
  fetch("/login").then(res => res.text()).then(text => {
    console.log(text)
  })
}

snippets = snippets.replaceAll("&#34;", "\"")
snippets = snippets.replaceAll("&#39;", "'")
snippets = JSON.parse(snippets)
if(snippets.length > 15){
  snippets = snippets.slice(0,15)
}
let score = 0
let index = 0
let outof = snippets.length
let snippet = snippets[index][0]
let artist = snippets[index][1]
let choices = [artist]
for(let i = 1; i < 4; i++){
  let rand = Math.floor(Math.random() * outof)
  if(snippets[rand][1] == artist || choices.includes(snippets[rand][1])){
    i-=1
  } 
  else{
    choices[i] = snippets[rand][1]
  }
}
choices = shuffle_choices(choices)
document.getElementById("number").innerHTML = (index+1) + "/" + outof
document.getElementById("question").innerHTML = "\"" + snippet + "\""
document.getElementById("song1").innerHTML = choices[0]
document.getElementById("song2").innerHTML = choices[1]
document.getElementById("song3").innerHTML = choices[2]
document.getElementById("song4").innerHTML = choices[3]
document.getElementsByClassName("choices").style.display = "flex"


function shuffle_choices(choices){
  for (var i = choices.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = choices[i];
        choices[i] = choices[j];
        choices[j] = temp;
    }
  return choices
}

function determineWin(choice){
  if(choice == artist){
    score += 1
  }
  index +=1
  if (index == outof){
    displayScore()
  }
  snippet = snippets[index][0]
  artist = snippets[index][1]
  choices = [artist]
  for(let i = 1; i < 4; i++){
    let rand = Math.floor(Math.random() * outof)
    if(snippets[rand][1] == artist || choices.includes(snippets[rand][1])){
      i-=1
    } 
    else{
      choices[i] = snippets[rand][1]
    }
  }
  choices = shuffle_choices(choices)
  document.getElementById("number").innerHTML = (index+1) + "/" + outof
  document.getElementById("question").innerHTML = "\"" + snippet + "\""
  document.getElementById("song1").innerHTML = choices[0]
  document.getElementById("song2").innerHTML = choices[1]
  document.getElementById("song3").innerHTML = choices[2]
  document.getElementById("song4").innerHTML = choices[3]
}

function displayScore(){
  document.getElementById("quiz").style.display = "none"
  document.getElementById("scoredisplay").style.display = "inline"
  document.getElementById("score").innerHTML = "Score: " + score + "/" + outof
} 
