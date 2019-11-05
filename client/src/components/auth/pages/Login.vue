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
          class="q-mt-sm bg-green-6 text-white"
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
import { setAuth, fetchUser } from '../../../store/state.js';

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
          localStorage.token = JSON.stringify(res.data.token);
          fetchUser();
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'You have been logged in. Welcome back.',
          });
        })
        .catch((err) => {
          if (err.response.status === 401) {
            this.$q.notify({
              color: 'negative',
              message: 'Invalid credentials. Please try again.',
              icon: 'report_problem',
            });
          } else {
            console.log(err);
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
          setAuth(true);
          this.$emit('login');
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
  },
};
</script>
