let navbar = document.querySelector('.navbar')
let burger = document.querySelector('.burger')
let leftNav = document.querySelector('.left-nav')
let rightNav = document.querySelector('.right-nav')
let name = document.querySelector('.name')

burger.addEventListener('click', () => {
    leftNav.classList.toggle('v-hidden-resp')
    rightNav.classList.toggle('v-hidden-resp')
    navbar.classList.toggle('resp-height')


})
