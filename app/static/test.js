var app = new Vue({
  el: '#app',
  data() {
    return {
      isis: false,
      response: {},
      length: 0,
      keycodition: false,
    }
  },
  async created() {
      await this.getData();
  },
  methods: {
      async getData() {
          let response = await axios.get('/get_data', {}, {})
             
          this.response = response.data;
          this.length = this.response.length - 1;
          },
      //addData() {
        //console.log('PUSH');
        //this.response.push(['5', 'ded', 'net']);
        //this.length += 1;
          //},
      checkLength(key) {
        return this.length === key
      }
  },
  computed: {

  },
  delimiters: ['[[', ']]'],
})