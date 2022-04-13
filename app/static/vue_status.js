var app = new Vue({
    el: '#app',
    data() {
      return {
        isAuth: false,
      }
    },
    async created() {
        const token = localStorage.getItem('token');

        if (token) {
            this.isAuth = true;
        }        

        await this.getData();
    },
    methods: {
        async getData() {
          try {
          
             let response = await axios.post('/protected', {}, {
                 headers: {
                     Authorization: 'Bearer ' + localStorage.getItem('token')
                 }
             })
             
             console.log("Sucess");

      
          }
          catch(error) {
              if (error.message === "Request failed with status code 403" || error.message === "Request failed with status code 422") {
                  this.isAuth = false;
                  localStorage.removeItem('token')
              };
              if (error.message === "Request failed with status code 401") {
                  //window.location="/login"
              }
          }
        } 
    },
    computed: {
      
    }
  })
  