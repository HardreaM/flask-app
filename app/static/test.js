var app = new Vue({
    el: '#app',
    data() {
      return {
        isis: false,
        response: {},
      }
    },
    async created() {
        await this.getData();
    },
    methods: {
        async getData() {
            let response = await axios.get('/get_data', {}, {})
               
            console.log(response.data);
            this.response = response.data;
            },
    },
    computed: {
      
    }
  })
  