<template>
  <div style="max-width: 90%" class="q-ml-auto q-mr-auto">
    <q-form id="loginForm" ref="loginForm" @submit.prevent.stop="login">
      <q-input outlined
        ref="email"
        type="email"
        label="Email"
        v-model="email"
        placeholder="youremail@email.com"
        color="green-6"
        :rules="[val => !!val || 'This field is required']"
        />
      <q-input outlined
        ref="password"
        type="password"
        label="Password"
        v-model="password"
        color="green-6"
        :rules="[val => !!val || 'This field is required']"
        />
      <div class="text-center">
        <q-btn
          label="Submit"
          type="submit"
          class="bg-green-6 text-white"
          />
        <br>
        <q-btn outline
          label="New user?"
          @click="toggle"
          size="sm" color="green-6"
          class="q-mt-sm"
          />
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    sendData(user) {
      this.$axios.post('/auth/login', { user })
        .then((res) => {
          this.$axios.defaults.headers.common.Authorization = `Bearer ${res.data.token}`;
          this.$store.state.token = res.data.token;
          this.$store.state.username = res.data.username;
          this.$store.state.isAuthenticated = true;
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: `Welcome back, ${this.$store.state.username}.`,
          });
          this.updateSession();
        })
        .catch((err) => {
          console.log(err);
          if (err.response.status === 404) {
            this.$q.notify({
              color: 'negative',
              message: 'Email not found.',
              icon: 'report_problem',
            });
          } else if (err.response.status === 401) {
            this.$q.notify({
              color: 'negative',
              message: 'Incorrect password.',
              icon: 'report_problem',
            });
          } else {
            this.$q.notify({
              color: 'negative',
              message: 'Login unsuccessful. Please try again.',
              icon: 'report_problem',
            });
          }
        });
    },
    login() {
      this.$refs.loginForm.validate(true)
        .then(() => {
          const user = { email: this.email, password: this.password };
          this.sendData(user);
          this.email = '';
          this.password = '';
          this.$refs.loginForm.reset();
        })
        .catch((err) => {
          console.log(err);
          this.$q.notify({
            color: 'negative',
            message: 'Invalid form data. Can not submit.',
            icon: 'report_problem',
          });
        });
    },
    toggle() {
      this.$emit('toggle');
    },
    updateSession() {
      this.$emit('update-session');
      console.log('le zession');
    },
  },
};
</script>
