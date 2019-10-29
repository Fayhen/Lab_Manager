<template>
  <div style="max-width: 90%" class="q-ml-auto q-mr-auto">
    <q-form ref="loginForm" @submit.prevent.stop="login">
      <q-input
        ref="email"
        type="email"
        label="Email"
        v-model="email"
        placeholder="youremail@email.com"
        standout="bg-green-3 text-white"
        :rules="[val => !!val || 'This field is required']"
        />
      <q-input
        ref="password"
        type="password"
        label="Password"
        v-model="password"
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
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    login() {
      this.$refs.loginForm.validate(true)
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
    },
  },
};
</script>
