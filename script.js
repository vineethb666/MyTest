function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange=function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("display").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "http://localhost:8080/QuerySearch/rest/Query/str", true);
  xhttp.send();
}

function postDoc() {
		  var xhttp = new XMLHttpRequest();
		  input = document.getElementById("display").value;
		  xhttp.onreadystatechange = function() {
		    if (this.readyState == 4 && this.status == 200) {
		      document.getElementById("display").innerHTML = this.responseText;
		    }
		  };
		  xhttp.open("GET", "http://192.168.1.10:9200/docs/_search?q="+input, true);
		 
		  xhttp.send();
	}