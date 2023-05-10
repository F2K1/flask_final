var under_1207p2px = window.matchMedia("(max-width: 1207.2px)");
var nav_btns = document.querySelectorAll(".navbar_groupR > a");
var ham_nav_btns = document.querySelector(".ham_menu");

function showHamMenuBtn(under_1207p2px) {
    if (under_1207p2px.matches) {
        for (let i = 0; i < nav_btns.length; i++) {
            nav_btns[i].style.display = "none";
        }
        document.getElementById("hamMenu").style.display = "block";
    } else {
        for (let i = 0; i < nav_btns.length; i++) {
            nav_btns[i].style.display = "inline-block";
        }
        document.getElementById("hamMenu").style.display = "none";
    }
}

showHamMenuBtn(under_1207p2px);
under_1207p2px.addEventListener("change", showHamMenuBtn)


function showHamMenu(comm) {
    if (comm == "show") {
        ham_nav_btns.style.display = "block";
    } else {
        ham_nav_btns.style.display = "none";
    }
}