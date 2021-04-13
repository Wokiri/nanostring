const DataSections = document.querySelectorAll(".data_sections")

DataSections.forEach((element, index) => {
    if (index % 2 === 0){
        element.classList.add("light-Aqua-BG")
    }else{
        element.classList.add("bg-light")
    }
});