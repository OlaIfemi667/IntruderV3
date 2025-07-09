const modal = document.getElementById('aiInfoModal');
const btn = document.getElementById('aiInfoBtn');
const span = modal.querySelector('.close');

btn.onclick = function() {
  modal.style.display = 'block';
}

span.onclick = function() {
  modal.style.display = 'none';
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}

