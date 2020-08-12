Vue.mixin( {  
  methods: {
	getParam : function(name){
		if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
			return decodeURIComponent(name[1]);
	},
	
	serialize : function(obj) {
	  var str = [];
	  for (var p in obj)
		if (obj.hasOwnProperty(p)) {
		  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		}
	  return str.join("&");
	},

    get : function(uri, params) {
	  var url = this.baseURL + uri;
	  	  
	  if(params) {
		url += '?' + this.serialize(params);
	  }
	  
	  console.log(`%cGET ${uri}`, 'background: blue; color: yellow', params);
	  
	  return fetch(url).then(response => response.json());
	},
	
	post : function(uri, params) {
	  var url = this.baseURL + uri;
	  console.log(`%POST ${uri} : `, 'background: blue; color: yellow', params);
	  
	  return fetch(url, {
			 method : 'POST',
			 headers : {'Content-Type': 'application/json'},
			 body : JSON.stringify(params)
		  }).then(response => response.json());
	},
  }
});