
const routes = [
  {
    path: '/',
    component: () => import('layouts/Layout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/personnel', component: () => import('pages/Personnel.vue') },
      { path: '/inventory', component: () => import('pages/Inventory.vue') },
      { path: '/fieldtrips', component: () => import('pages/Fieldtrips') },
      { path: '/news', component: () => import('pages/News') },
      { path: '/calendar', component: () => import('pages/Calendar') },
      { path: '/notices', component: () => import('pages/Notices') },
    ],
  },
];

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue'),
  });
}

export default routes;
