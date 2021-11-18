import './style.css'

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];


var access_level = 0;
var protected_link = document.getElementsByClassName("protected_link");
console.log(protected_link);

for(var x = 0; x < protected_link.length; x++){
  protected_link[x].onclick = function(){
    if(access_level != 0){
      window.alert("You do not have the right access for this");
      return false;
    }
  }
}

document.getElementById("access_change").onclick = function(){
  access_level = 2;
}

document.getElementById("test").onclick = function(){
  console.log("hello"); 
}


document.getElementById('login').onclick = function(){
  console.log("hello?");
  modal.style.display = "block";
};

document.getElementById("login_submit").onclick = function(){
  console.log("submit button pressed");
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}


function accessMyVariable(){
  access_level = 0;
}
