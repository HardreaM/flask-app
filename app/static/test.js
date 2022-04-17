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
             
          this.response = response.data;
          },
      addData() {
        this.response.push(['5', 'ded', 'net']);
      },
  },
  computed: {

  },
  delimiters: ['[[', ']]'],
})