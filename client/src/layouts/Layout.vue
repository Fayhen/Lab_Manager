<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-green-6 text-white">
      <q-toolbar>
        <q-toolbar-title class="apptitle">
          <q-avatar>
            <img src="~/assets/AppIconBackgroundWhite.svg" width="20">
          </q-avatar>
            Laborator.io
        </q-toolbar-title>

        <q-tabs align="left" v-model="tab" shrink>
          <q-route-tab to="/" label="Home" />
          <q-route-tab to="/personnel" label="Personnel" />
          <q-route-tab to="/inventory" label="Inventory" />
          <q-route-tab to="/fieldtrips" label="Fieldtrips" />
          <q-route-tab to="/calendar" label="Calendar" />
        </q-tabs>

        <q-btn dense flat round icon="menu" @click="right = !right" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="right" side="right" bordered>
      <auth />
      <notices class="hidden" />
      <news class="hidden" />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white apptitle">
      <q-toolbar>
        <q-toolbar-title class="text-body2">
          Laborator.io - v.0.0.x
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
