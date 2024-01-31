document.addEventListener('DOMContentLoaded', function () {
    let nextDom = document.querySelector(".arrows #next");
    let prevDom = document.querySelector(".arrows #prev");
    let carouselDom = document.querySelector('.carousel');
    let listItemDom = document.querySelector('.carousel .list'); 
    let thumbNailDom = document.querySelector('.carousel .thumbnail'); 

    if (nextDom) {
        nextDom.addEventListener('click', function () {
            showSlider('next');
        });
    }

    if (prevDom) {
        prevDom.addEventListener('click', function () {
            showSlider('prev');
        });
    }

    let timeRunning = 3000;
    let timeAutoNext = 7000;
    let timeRunOut;
    let runAutoRun = setTimeout(() => {
        nextDom.click(); 
    }, timeAutoNext);

    function showSlider(type) {
        let itemSlider = document.querySelectorAll('.carousel .list .item');
        let itemThumbnail = document.querySelectorAll('.carousel .thumbnail .item');

        if (type === 'next') {
            listItemDom.appendChild(itemSlider[0].cloneNode(true));
            listItemDom.removeChild(itemSlider[0]);

            thumbNailDom.appendChild(itemThumbnail[0].cloneNode(true));
            thumbNailDom.removeChild(itemThumbnail[0]);

            carouselDom.classList.add('next');
        } else {
            let positionLastItem = itemSlider.length - 1;
            listItemDom.prepend(itemSlider[positionLastItem].cloneNode(true));
            listItemDom.removeChild(itemSlider[positionLastItem]);

            thumbNailDom.prepend(itemThumbnail[positionLastItem].cloneNode(true));
            thumbNailDom.removeChild(itemThumbnail[positionLastItem]);

            carouselDom.classList.add('prev');
        }

        clearTimeout(timeRunOut);
        timeRunOut = setTimeout(() => {
            carouselDom.classList.remove("next");
            carouselDom.classList.remove("prev");
        }, timeRunning);

        clearTimeout(runAutoRun);
    }
});

