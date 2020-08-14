Vue.mixin({
  data: function() {
    return {
      baseURL: 'http://127.0.0.1:8000/api',
      token: null,
    }
  },
  created: function() {
    this.token = localStorage.getItem('token');
  },
  methods: {
    logOut() {
      localStorage.removeItem('token');
      location.href = '/login.html';
    },

    getParam: function (name) {
      if (name = (new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
    },

    serialize: function (obj) {
      var str = [];
      for (var p in obj)
        if (obj.hasOwnProperty(p)) {
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
      return str.join("&");
    },

    get: function (uri, params) {
      var url = this.baseURL + uri;

      if (params) {
        url += '?' + this.serialize(params);
      }

      console.log(`%cGET ${uri}`, 'background: blue; color: yellow', params);

      return fetch(url).then(response => response.json());
    },

    post: function (uri, data, isFormData) {
      var url = this.baseURL + uri;
      console.log(`%POST ${uri} : `, 'background: blue; color: yellow', data);
      var headers = {};
      if(localStorage.getItem('token')) {
        headers['Authorization'] = 'Bearer ' + localStorage.getItem('token');
      }

      if (!isFormData) {
        headers['Content-Type'] = 'application/json';
        return fetch(url, {
          method: 'POST',
          headers:headers,
          body: JSON.stringify(data)
        }).then(response => response.json());
      } else {
        return fetch(url, {
          method: 'POST',
          headers:headers,
          body: data
        }).then(response => response.json());
      }
    },
  }
});