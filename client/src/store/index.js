import Vue from 'vue';

export default function () {
  const state = Vue.observable({
    token: null,
    isAuthenticated: false,
  });
  Vue.prototype.$store = { state };

  return state;
}
