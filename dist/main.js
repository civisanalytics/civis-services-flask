const fetchAndUpdate = function (endpoint, elementID) {
  let Http = new XMLHttpRequest();
  Http.open("GET", endpoint);
  Http.send();
  Http.onreadystatechange = () => {
    document.getElementById(elementID).innerHTML = Http.responseText;
  };
};

// Here we hit the /fruits endpoint on our Service that returns JSON that we then display it on our HTML page
const apiEndpoint = window.location.origin + "/api/fruits";
document.getElementById("api-endpoint").innerHTML = apiEndpoint;
fetchAndUpdate(apiEndpoint, "entry-point");

const healthEndpoint = window.location.origin + "/api/health";
fetchAndUpdate(healthEndpoint, "service-id");
