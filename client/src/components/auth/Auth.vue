<template>
  <div class="q-mt-sm text-center text-body-1">
    <user-card v-bind:class="{ hidden: !showAuth }"
      @logout="userOut()" />
    <div class="q-mt-sm" v-bind:class="{ hidden: showAuth }">
      <p>Welcome, visitor!</p>
      <p>Please log in to use Laborator.io</p>
      <login-form v-bind:class="{ hidden: showLogin }"
        @toggle="toggle()" @login="userIn()" />
      <register-form v-bind:class="{ hidden: showRegister }"
        @toggle="toggle()" />
    </div>
    <div>
    </div>
    <test-server @logout="userOut()" />
  </div>
</template>

<script>
import TestServer from './TestServer';
import LoginForm from './pages/Login.vue';
import RegisterForm from './pages/Register.vue';
import UserCard from './pages/UserCard.vue';

export default {
  name: 'Auth',
  data() {
    return {
      showAuth: false,
      showLogin: false,
      showRegister: true,
    };
  },
  mounted() {
    if (localStorage.token) {
      this.showAuth = true;
    }
  },
  methods: {
    toggle() {
      this.showLogin = !this.showLogin;
      this.showRegister = !this.showRegister;
    },
    userIn() {
      this.showAuth = true;
    },
    userOut() {
      this.showAuth = false;
      this.$router.push('/');
    },
  },
  components: {
    TestServer,
    LoginForm,
    RegisterForm,
    UserCard,
  },
};
</script>
