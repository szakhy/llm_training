import { createRouter, createWebHistory } from 'vue-router';
import ProductList from '../views/ProductList.vue';
import ProductDetail from '../views/ProductDetail.vue';
import CreateProduct from '../views/CreateProduct.vue';

const routes = [
  {
    path: '/',
    redirect: '/products'
  },
  {
    path: '/products',
    name: 'ProductList',
    component: ProductList
  },
  {
    path: '/products/create',
    name: 'CreateProduct',
    component: CreateProduct
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: ProductDetail
  },
  {
    path: '/products/:id/edit',
    name: 'EditProduct',
    component: ProductDetail
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
