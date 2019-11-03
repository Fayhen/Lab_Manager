<template>
  <div class="q-mt-sm text-center text-body-1">
    <div v-bind:class="{ hidden: !isAuthenticated }">
      <p>Welcome, {{ username }}</p>
      <q-btn
        label="Logout"
        type="submit"
        class="bg-green-6 text-white"
        @click="logout"
        />
    </div>
    <div class="q-mt-sm" v-bind:class="{ hidden: isAuthenticated }">
      <p>Welcome, visitor!</p>
      <p>Please log in to use Laborator.io</p>
      <login-form
        @toggle="toggle()" @update-session="update()"
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
import LoginForm from './forms/Login.vue';
import RegisterForm from './forms/Register.vue';

export default {
  name: 'Auth',
  data() {
    return {
      isAuthenticated: false,
      username: null,
      showLogin: false,
      showRegister: true,
    };
  },
  methods: {
    toggle() {
      this.showLogin = !this.showLogin;
      this.showRegister = !this.showRegister;
    },
    update() {
      this.isAuthenticated = this.$store.state.isAuthenticated;
      this.username = this.$store.state.username;
    },
    logout() {
      this.$store.state.token = null;
      this.$store.state.username = null;
      this.$store.state.isAuthenticated = false;
      this.update();
    },
  },
  components: {
    TestServer,
    LoginForm,
    RegisterForm,
  },
};
</script>
