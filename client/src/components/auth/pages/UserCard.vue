<template>
  <div>
      <q-card flat square>
      <q-img src="https://cdn.quasar.dev/img/parallax2.jpg">
        <div class="absolute-bottom">
          <div class="text-h6">{{ user.username }}</div>
          <div class="text-subtitle2">{{ user.email }}</div>
        </div>
      </q-img>

      <q-card-actions align="right">
        <q-btn outline
        label="My Profile"
        type="submit"
        size="sm" color="green-6"
        />
        <q-btn outline
        label="Logout"
        type="submit"
        size="sm" color="green-6"
        class="q-ml-sm"
        @click="endSession()"
        />
      </q-card-actions>
    </q-card>
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
    console.log('mounted hook at UserCard calling update()');
    update();
  },
  methods: {
    endSession() {
      logout();
      this.$emit('logout');
    },
  },
};
</script>
