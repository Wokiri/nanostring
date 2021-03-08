const servicesDiv = document.querySelector("#servicesDiv")

if (servicesDiv){

    const serviceSections = servicesDiv.querySelectorAll(".serviceSections")


    for (let num = 0; num < serviceSections.length; num++){
        if (num % 2 === 0){
            serviceSections[num].classList.add("fromLeft")
        }
        else{
            serviceSections[num].classList.add("fromRight")
        }
    }

    const sectionsObserverOptions = {
        root: null,
        rootMargin: "0px 0px 0px 0px",
        threshold: 0.25
    }

    const animateServices = () => {
        const Observer = new IntersectionObserver((sectionsEntry) => {

                sectionsEntry.forEach((entry) => {

                    if (!entry.isIntersecting) {
                        entry.target.classList.remove("normal")
                        return
                    }

                    entry.target.classList.add("normal")
                })
            },
            sectionsObserverOptions)

        serviceSections.forEach(appear => {
            Observer.observe(appear)
        })

    }

    window.addEventListener("load", () => {
        if (servicesDiv) animateServices()
    }, false)
}
