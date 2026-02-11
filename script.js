const notes = document.getElementById("notes");
const input = document.getElementById("commandInput");
const slides = document.querySelectorAll(".slide");

let slideIndex = 0;

function switchBoard() {
    document.getElementById("pptMode").classList.remove("active");
    document.getElementById("boardMode").classList.add("active");
    modeText.innerText = "Board Mode";
}

function switchPPT() {
    document.getElementById("boardMode").classList.remove("active");
    document.getElementById("pptMode").classList.add("active");
    modeText.innerText = "PPT Mode";
}

function runCommand() {
    if (!input.value.trim()) return;

    const p = document.createElement("p");
    p.textContent = input.value;
    notes.appendChild(p);
    input.value = "";
}

function clearAll() {
    notes.innerHTML = "";
}

function nextSlide() {
    slides[slideIndex].classList.remove("active");
    slideIndex = (slideIndex + 1) % slides.length;
    slides[slideIndex].classList.add("active");
}

function prevSlide() {
    slides[slideIndex].classList.remove("active");
    slideIndex = (slideIndex - 1 + slides.length) % slides.length;
    slides[slideIndex].classList.add("active");
}

function setDark() {
    document.body.classList.add("dark");
}

function setLight() {
    document.body.classList.remove("dark");
}
