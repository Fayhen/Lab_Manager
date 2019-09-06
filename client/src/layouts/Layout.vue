<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg" width="20">
          </q-avatar>
            Laborator.io
        </q-toolbar-title>

        <q-tabs align="left" v-model="tab" shrink>
          <q-route-tab to="/" label="Home" />
          <q-route-tab to="/personnel" label="Personnel" />
          <q-route-tab to="/inventory" label="Inventory" />
          <q-route-tab to="/fieldtrips" label="Fieldtrips" />
          <q-route-tab to="/news" label="News" />
          <q-route-tab to="/calendar" label="Calendar" />
        </q-tabs>

        <q-btn dense flat round icon="menu" @click="right = !right" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="right" side="right" bordered>
      <!-- Notices drawer content -->
      <auth />
      <notices />
      <news />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          Laborator.io
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import Auth from '../components/auth/Auth';
import Notices from '../components/notices/Notices';
import News from '../components/news/News';

export default {
  name: 'Layout',
  components: { Notices, Auth, News },
  data() {
    return {
      right: true,
    };
  },
};
</script>

<style>
</style>
