<template>
  <q-page>
    {{ msg }}
  </q-page>
</template>

<script>
export default {
  name: 'Auth',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    loadData() {
      this.$axios.get('http://127.0.0.1:5000/auth/test')
        .then((response) => {
          this.msg = response.data;
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Server connection failed',
            icon: 'report_problem',
          });
        });
    },
  },
  created() {
    this.loadData();
  },
};
</script>
