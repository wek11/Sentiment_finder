// Observer to check whether an element is on the screen and if so, adds show class
// If not, removes show class
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

// Gathers elements with class hidden and sends them through the observer
const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

let deleteMe = (ele, id) => {
    $.ajax({
        url: "http://127.0.0.1:8000/sentiment/delete/".concat(id),
        type: 'POST',
        data : {
            name:"name",
            csrfmiddlewaretoken: '{{ csrf_token }}' , //This is must for security in Django
        }, 
        success : function(response){
            ele.parentNode.remove();
        },
        error: function (error){},

    })
}   