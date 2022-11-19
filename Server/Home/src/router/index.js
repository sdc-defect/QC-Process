import Vue from "vue";
import VueRouter from "vue-router";

import LandingPage from "../views/landing.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/land",
    name: "landing",
    component: LandingPage,
  },
];

const router = new VueRouter({
  mode: "history",
  //   base: process.env.BASE_URL,
  routes,
});

export default router;
