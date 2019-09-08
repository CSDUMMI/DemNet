
const app          = new Vue({
  el: '#app',
  data: {
    feed_content : "Nothing here"
  }
});

let request        = new XMLHttpRequest();


request.responseType  = 'json';

request.addEventListener('load', () => {
  app.feed_content = this.response;
});

request.open( 'POST', '/feed');
request.send();


function add_content(content, content_type ) {
  request.open('POST', '/create');

}

function follow( username ) {
  request.open('POST', '/create');
  request.send
}
