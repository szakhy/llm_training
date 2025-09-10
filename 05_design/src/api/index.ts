// --- Cart Types ---
export interface CartItemDTO {
  id: number;
  product: Product;
  quantity: number;
}

export interface CartDTO {
  id: number;
  items: CartItemDTO[];
}

export interface CartItemAdd {
  product_id: number;
  quantity: number;
}
export const cartApi = {
  getCart: () => apiClient.get<CartDTO>('/cart'),
  createCart: () => apiClient.post<CartDTO>('/cart/create'),
  addItem: (item: CartItemAdd) => apiClient.post<CartDTO>('/cart/add', item),
  removeItem: (item: CartItemAdd) => apiClient.post<CartDTO>('/cart/remove', item),
  updateQuantity: (item: CartItemAdd) => apiClient.post<CartDTO>('/cart/update', item),
};
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Product {
  id: number;
  name: string;
  price: number;
  description?: string;
  stock: number;
}

export interface CreateProductDTO {
  name: string;
  price: number;
  description?: string;
  stock: number;
}

export const productApi = {
  getProducts: () => apiClient.get<Product[]>('/products'),
  getProduct: (id: number) => apiClient.get<Product>(`/products/${id}`),
  createProduct: (product: CreateProductDTO) => apiClient.post<Product>('/products', product),
  updateProduct: (id: number, product: CreateProductDTO) => apiClient.put<Product>(`/products/${id}`, product),
  deleteProduct: (id: number) => apiClient.delete(`/products/${id}`),
};

export default apiClient;
