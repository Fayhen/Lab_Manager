<template>
  <div style="max-width: 90%" class="q-ml-auto q-mr-auto">
    <q-form ref="registerForm" @submit.prevent.stop="register">
      <q-input outlined
        ref="username"
        label="Username"
        v-model="username"
        placeholder="Your desired username"
        color="green-6"
        counter maxlength="30"
        :rules="[
          val => !!val || 'This field is required',
          val => val.length <= 30 || 'Please use maximum 30 characters'
          ]"
        />
      <q-input
        ref="email" outlined
        type="email"
        label="Email"
        v-model="email"
        placeholder="youremail@email.com"
        color="green-6"
        counter maxlength="30"
        :rules="[
          val => !!val || 'This field is required',
          val => val.length <= 30 || 'Please use maximum 30 characters'
          ]"
        />
      <q-input outlined
        ref="password"
        type="password"
        label="Password"
        v-model="password"
        color="green-6"
        counter maxlength="12"
        :rules="[val => !!val || 'This field is required']"
        />
      <q-input outlined
        ref="confirmPassword"
        type="password"
        label="Confirm password"
        v-model="confirmPassword"
        color="green-6"
        :rules="[
          val => val === password || 'Passwords do no match',
          val => !!val || 'This field is required'
          ]"
        />
      <div class="text-center">
        <q-btn
          label="Submit"
          type="submit"
          class="q-mt-sm bg-green-6 text-white"
          />
        <br>
        <q-btn outline
          label="Already registered?"
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
    sendData(newUser) {
      this.$axios.post('/auth/add', newUser)
        .then((res) => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: `Account created for ${res.data.username}. You can now log in.`,
          });
          this.toggle();
        })
        .catch((err) => {
          if (err.response.status === 409) {
            this.$q.notify({
              color: 'negative',
              message: 'Username or email already exists. Please try using other ones.',
              icon: 'report_problem',
            });
          } else {
            this.$q.notify({
              color: 'negative',
              message: 'Registration unsuccessful. Please try again.',
              icon: 'report_problem',
            });
          }
        });
    },
    register() {
      this.$refs.registerForm.validate(true)
        .then(() => {
          const newUser = {
            username: this.username,
            email: this.email,
            password: this.password,
          };
          this.sendData(newUser);
          this.username = '';
          this.email = '';
          this.password = '';
          this.confirmPassword = '';
          this.$refs.registerForm.reset();
        })
        .catch(() => {
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
