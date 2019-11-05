<template>
  <div class="q-mt-sm text-center text-body-1">
    <user-card
      @logout="toggleUserCard()" v-bind:class="{ hidden: !showAuth }" />
    <div class="q-mt-sm" v-bind:class="{ hidden: showAuth }">
      <p>Welcome, visitor!</p>
      <p>Please log in to use Laborator.io</p>
      <login-form
        @toggle="toggle()" @login="toggleUserCard()"
        v-bind:class="{ hidden: showLogin }" />
      <register-form
        @toggle="toggle()" v-bind:class="{ hidden: showRegister }" />
    </div>
    <div>
    </div>
    <test-server />
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
    toggleUserCard() {
      this.showAuth = !this.showAuth;
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
