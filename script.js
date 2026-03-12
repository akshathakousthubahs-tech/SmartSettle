async function upload(){

let file=document.getElementById("file").files[0];

let formData=new FormData();

formData.append("file",file);

let response = await fetch("/upload",{

method:"POST",
body:formData

});

let data = await response.json();

document.getElementById("output").innerText =
JSON.stringify(data,null,2);

}

function download(){

window.location="/download";

}
