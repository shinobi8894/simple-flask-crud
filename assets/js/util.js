const gridBtn = document.querySelector('.grid-btn');
const columnBtn = document.querySelector('.column-btn');
const viewItems = document.querySelectorAll('.view-item');
const blogList = document.querySelector('#blog-list');
const publishPostBtn = document.querySelector('.publish-post');
const postCaptionArea = document.querySelector('#post-caption');
const postImg = document.querySelector('#post-img');
const uploadPostBtn = document.querySelector('#upload-post');

const removeActive = () => {
    viewItems.forEach(element => element.classList.remove('active'));
}

const loadPost = () => {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    
    xhr.addEventListener("readystatechange", function() {
      if(this.readyState === 4) {
        renderCard(this.responseText)
      }
    });
    
    xhr.open("POST", "http://localhost:3000/load");
    xhr.send();
}

const createBlogCard = (data, key) => {
    const card = document.createElement('div');
    const cardHeader = document.createElement('div');
    const cardbody = document.createElement('div');
    const cardFooter = document.createElement('div');
    const caption = document.createElement('p');
    const heading = document.createElement('h2');
    const postImg = document.createElement('img')
    card.classList.add('card', 'col-5');
    cardHeader.classList.add('card-header', 'd-flex', 'justify-content-between', 'align-items-center');
    cardbody.classList.add('card-body', 'p-0')
    cardFooter.classList.add('card-footer')
    postImg.src=data.url;
    postImg.classList.add('img-fluid');
    postImg.alt="post"
    heading.innerHTML=key+1;
    caption.innerHTML=data.caption;
    cardHeader.appendChild(heading);
    cardbody.appendChild(postImg);
    cardFooter.appendChild(caption);
    card.appendChild(cardHeader);
    card.appendChild(cardbody)
    card.appendChild(cardFooter)
    return card;
}

const renderCard = (data) => {
    JSON.parse(data).map((element,key) => {
        blogList.appendChild(createBlogCard(element, key))
    })
}

const showGrid = (e) => {
    removeActive();
    e.currentTarget.querySelector('svg').classList.add('active')
    blogList.classList.add('grid-list')
}

const showColumn = (e) => {
    removeActive();
    e.currentTarget.querySelector('svg').classList.add('active')
    blogList.classList.remove('grid-list')
}

const addNewPost = () => {

    var data = new FormData();
    data.append("postImg", postImg.files[0]);
    data.append("caption", postCaptionArea.value);
    
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    
    xhr.addEventListener("readystatechange", function() {
      if(this.readyState === 4) {
        console.log(this.responseText);
      }
    });
    
    xhr.open("POST", "http://localhost:3000/new");
    xhr.send(data);
}

(function () {
    gridBtn.addEventListener('click', (e) => showGrid(e));
    columnBtn.addEventListener('click', (e) => showColumn(e));
    publishPostBtn.addEventListener('click', (e) => addNewPost(e));
    uploadPostBtn.addEventListener('click', () => postImg.click());
    window.addEventListener('load', loadPost)
    postImg.style.display="none";
})();



