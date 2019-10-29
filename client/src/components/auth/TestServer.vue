<template>
  <div></div>
</template>

<script>
export default {
  name: 'TestServer',
  data() {
    return {
      status: '',
    };
  },
  methods: {
    testServer() {
      this.$axios.get('http://127.0.0.1:5000/auth/test')
        .then((response) => {
          this.status = response.data;
          console.log(this.status);
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Server is offline',
            icon: 'report_problem',
          });
        });
    },
  },
  created() {
    this.testServer();
  },
};
</script>
