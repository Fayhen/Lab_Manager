<template>
  <div>
    <q-toolbar class="column">
      <div class="full-width row justify-between ">
        <div class="text-h6 text-green-10 text-weight-regular">
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
          </q-avatar>
          {{ user.username }}
        </div>
        <div class="justify-end">
          <q-btn flat round color="green-6" icon="perm_identity"
            @click="openProfile()" />
          <q-btn flat round color="green-6" icon="exit_to_app"
            @click="endSession()"/>
        </div>
      </div>
    </q-toolbar>
  </div>
</template>

<script>
import {
  getAuth, getUser, update, logout,
} from '../../../store/state.js';

export default {
  name: 'UserCard',
  computed: {
    isAuthenticated() {
      return getAuth();
    },
    user() {
      return getUser();
    },
  },
  mounted() {
    update('UserCard component on Auth module.');
  },
  methods: {
    openProfile() {
      this.$router.push('/profile');
    },
    endSession() {
      logout();
      this.$emit('logout');
    },
  },
};
</script>
