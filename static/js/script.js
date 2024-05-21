let eyeIcon = document.getElementById('eye-icon')
let password = document.getElementById('password')


eyeIcon.onclick = function () {
  if (password.type == 'password' ) {
    password.type = 'text'
  
    eyeIcon.src = '../img/eye-show.png'
  } else {
    password.type = 'password'
   
    eyeIcon.src = '../img/eye-close.png'
  }
}


modal = getElementById('modal')
closeButton = getElementById('close-modal-btn')

// load pop on page load
window.onload = function () {
  
}


const LoadPopup = function () {
  window.addEventListener('load', modal.classList.remove('hidden'))
} 


document
  .getElementById('open-modal-btn')
  .addEventListener('onLoad', function () {
    document.getElementById('modal').classList.remove('hidden')
  })

document
  .getElementById('close-modal-btn')
  .addEventListener('click', function () {
    document.getElementById('modal').classList.add('hidden')
  })




  document.addEventListener('DOMContentLoaded', () => {
    const openModalBtn = document.getElementById('openModal')
    const closeModalBtn = document.getElementById('closeModal')
    const modal = document.getElementById('modal')

    openModalBtn.addEventListener('click', () => {
      modal.classList.remove('hidden')
    })

    closeModalBtn.addEventListener('click', () => {
      modal.classList.add('hidden')
    })
  })