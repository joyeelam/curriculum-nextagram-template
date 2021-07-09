// function for homepage carousel
$(document).ready(function() {
  $('.carousel').carousel({
    interval: 5000
  })
})

// function for posts preview
let previewImage = function(event) {
  let preview = document.getElementById('preview')
  preview.src = URL.createObjectURL(event.target.files[0])
  preview.style.display = "block"
}
