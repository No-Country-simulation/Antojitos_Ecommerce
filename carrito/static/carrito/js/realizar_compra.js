let selectedOption = '';

function selectOption(option) {
  selectedOption = option;
  document.querySelectorAll('.list-group-item').forEach(item => {
    item.classList.remove('active');
  });
  event.currentTarget.classList.add('active');
}

function saveSelection() {
  document.getElementById('selectedOption').innerText = `Has seleccionado: ${selectedOption}`;
}
