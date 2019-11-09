
const routes = [
  {
    path: '/',
    component: () => import('layouts/Layout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/personnel', component: () => import('components/personnel/Personnel.vue') },
      { path: '/inventory', component: () => import('components/inventory/Inventory.vue') },
      { path: '/fieldtrips', component: () => import('components/fieldtrips/Fieldtrips') },
      { path: '/calendar', component: () => import('components/calendar/Calendar') },
      { path: '/news', component: () => import('components/news/News') },
      { path: '/notices', component: () => import('components/notices/Notices') },
      { path: '/profile', component: () => import('components/auth/pages/Profile') },
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
