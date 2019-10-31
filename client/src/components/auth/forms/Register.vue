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
      this.$refs.registerForm.validate(true)
        .then(() => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Submitted',
          });
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            message: 'There is a problem in the form.',
            icon: 'report_problem',
          });
        });

      const newUser = {
        username: this.username,
        email: this.email,
        password: this.password,
      };

      this.$axios.post('/auth/add', newUser)
        .then((res) => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: `Account created for ${res.data.username}.`,
          });
        });

      // Object.assign(this.$data, this.$options.data());
      // this.$refs.registerForm.resetValidation();
    },
  },
};
</script>
