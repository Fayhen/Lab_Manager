<template>
  <div>
    <test-server />
    <login-form />
    <register-form />
  </div>
</template>

<script>
import TestServer from './TestServer';
import LoginForm from './forms/Login.vue';
import RegisterForm from './forms/Register.vue';

export default {
  name: 'Auth',
  components: {
    TestServer,
    LoginForm,
    RegisterForm,
  },
};
</script>
