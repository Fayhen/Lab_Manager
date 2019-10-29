<template>
  <div style="max-width: 90%" class="q-ml-auto q-mr-auto">
    <q-form ref="registerForm" @submit.prevent.stop="register">
      <q-input
        ref="username"
        label="Username"
        placeholder="Your desired username"
        v-model="username"
        counter maxlength="30"
        standout="bg-green-3 text-white"
        :rules="[
          val => !!val || 'This field is required',
          val => val.length <= 30 || 'Please use maximum 30 characters'
          ]"
        />
      <q-input
        ref="email"
        type="email"
        label="Email"
        placeholder="youremail@email.com"
        v-model="email"
        counter maxlength="30"
        standout="bg-green-3 text-white"
        :rules="[
          val => !!val || 'This field is required',
          val => val.length <= 30 || 'Please use maximum 30 characters'
          ]"
        />
      <q-input
        ref="password"
        type="password"
        label="Password"
        v-model="password"
        counter maxlength="12"
        standout="bg-green-3 text-white"
        :rules="[val => !!val || 'This field is required']"
        />
      <q-input
        ref="confirmPassword"
        type="password"
        label="Confirm password"
        v-model="confirmPassword"
        standout="bg-green-3 text-white"
        :rules="[
          val => val === password || 'Passwords do no match',
          val => !!val || 'This field is required'
          ]"
        />
      <div class="text-center">
        <q-btn
          label="Submit"
          type="submit"
          class="bg-green-6 text-white"
          />
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    register() {
      // this.$refs.username.validate();
      // this.$refs.email.validate();
      // this.$refs.password.validate();
      // this.$refs.confirmPassword.validate();

      // if (
      //   this.$refs.username.hasError
      //   || this.$refs.email.hasError
      //   || this.$refs.password.hasError
      //   || this.$refs.confirmPassword.hasError
      // ) {
      //   this.formHasError = true;
      // } else {
      //   this.$q.notify({
      //     icon: 'done',
      //     position: 'top',
      //     color: 'positive',
      //     message: 'Submitted',
      //   });
      // }
      this.$refs.registerForm.validate(true)
        .then(() => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Submitted',
          });
        });
    },
  },
};
</script>
