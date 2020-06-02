let i;
selected_images = document.getElementsByClassName("select-image")
for (i = 0; i < selected_images.length; i++){
    let p = i + 1;
    selected_images[i].setAttribute("onclick", "current_slide(" + p + ")");
}


let slide_index = 1;

function plus_slide(n){
    show_slides(slide_index+=n);
}

function current_slide(n){
    show_slides(n);
}


function show_slides(n) {
    let i;
    let slides = document.getElementsByClassName("main-image");
    let selected_images = document.getElementsByClassName("select-image");
    slide_index = n;

    if (n > slides.length){
        slide_index = 1;
    }

    if (n < 1){
        slide_index = slides.length;
    }

    for (i = 0; i < slides.length; i++){
        slides[i].style.display = "none";
    }

    for (i = 0; i < selected_images.length; i++){
        selected_images[i].className = "select-image";
        let p = i + 1;
        selected_images[i].setAttribute("onclick", "current_slide(" + p + ")");
    }

    slides[slide_index - 1].style.display = "block";
    selected_images[slide_index - 1].className += " selected";
}
