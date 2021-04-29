$('form input[type="file"]').change(event => {
  let files = event.target.files;
  if (files.length !== 0) {
    if(files[0].type == 'image/jpeg') {
      $('img').remove();
      let image = $('<img>');
      image.attr('src', window.URL.createObjectURL(files[0]));
      $('figure').prepend(image);
    } else {
      alert('Unsupported file format')
    }
  }
});