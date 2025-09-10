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
