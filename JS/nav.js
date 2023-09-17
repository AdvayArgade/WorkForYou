function navigationLoader(){
    fetch('nav.html')
    .then(response => response.text())
        .then(data => {
            document.getElementById('nav').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading navigation:', error);
        });
}
document.addEventListener('DOMContentLoaded',navigationLoader);
