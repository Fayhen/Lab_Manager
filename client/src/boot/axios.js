import axios from 'axios';

export default async ({ Vue }) => {
  Vue.prototype.$axios = axios;

  axios.defaults.baseURL = 'http://localhost:5000';
  axios.defaults.headers.common.Authorization = null;
};
