//navbar
const navbar = document.querySelector(".navbar_left");
const navbarIcons = document.querySelector(".navbar_menu");
//to open and close
navbarIcons.addEventListener("click", () => {
  navbar.classList.toggle("navbar_show");
});

const searchBar = document.querySelector(".searchbar");
const error = document.querySelector(".input_box p");
const inputBox = document.querySelector(".input_box input");
const button = document.querySelector(".searchbar button");
const urlDiv = document.querySelector(".url_links");
const data = localStorage.getItem("_html");
if (!data) {
  localStorage.setItem("_html", "[]");
}




inputBox.addEventListener("focus", (e) => {
  window.addEventListener("keydown", (e) => {
    if (e.key == "Enter") {
      searhApi(inputBox.value);
      inputBox.value = null;
    }
  });
});

showHtml();
