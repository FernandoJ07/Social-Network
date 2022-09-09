function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function editPost(id){

    const info = document.querySelector(`#info-${id }`);
    const formEditContent = document.querySelector(`#formEdit-content-${id}`);

    // show form edit post
    info.classList.add('visually-hidden');
    formEditContent.classList.remove('visually-hidden');

    // button closeForm 
    document.querySelector(`#closeForm-${id}`).addEventListener('click', () => {
        info.classList.remove('visually-hidden');
        formEditContent.classList.add('visually-hidden');
    })

    // sending information to server
    document.querySelector(`#saveForm-${id}`).addEventListener('click', () => {
        fetch(`http://127.0.0.1:8000/edit/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                form: document.querySelector(`#contentPost-${id}`).value
            }),
            headers: {'X-CSRFToken': getCookie('csrftoken'),} 
        })
        .then(response => response.json())
        .then((post) => {

            // show info
            info.classList.remove('visually-hidden');
            formEditContent.classList.add('visually-hidden');
    
            document.querySelector(`#postContent-${id}`).innerHTML = post.content

            
        })

    })
}

function like(id){
    
    if(document.querySelector(`#heart-${id}`).name == 'heart-outline'){


        fetch(`http://127.0.0.1:8000/like/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                like: true
            }),
            headers: {'X-CSRFToken': getCookie('csrftoken'),} ,
            referrerPolicy: "origin-when-cross-origin"
    
        })
        .then(response => response.json())
        .then((like) => {
            document.querySelector(`#like-${id}`).innerHTML = like.like
        })
    
        document.querySelector(`#heart-${id}`).name = 'heart';

    }else{

        fetch(`http://127.0.0.1:8000/like/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                like: false
            }),
            headers: {'X-CSRFToken': getCookie('csrftoken'),} 
    
        })
        .then(response => response.json())
        .then((like) => {
    
            document.querySelector(`#like-${id}`).innerHTML = like.like
            
        })  
        
        document.querySelector(`#heart-${id}`).name = 'heart-outline';

    }
    
}



