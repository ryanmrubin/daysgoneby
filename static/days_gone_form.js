window.onload = function() {
  for (i = 0, fieldRows = document.getElementsByClassName('form-field'), len = fieldRows.length;
       i < len;
       i++) {
    row = fieldRows[i];
    for (j = 0, inputs = row.getElementsByTagName('input'), rowLength = inputs.length, j < rowLength;
         j < rowLength;
         j++) {
      input = inputs[j];
      input.disabled = true;
    }
  }
}
