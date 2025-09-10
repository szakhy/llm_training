<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { productApi, type Product, type CreateProductDTO } from '../api';

const route = useRoute();
const router = useRouter();
const product = ref<Product | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const saving = ref(false);
const isEditMode = ref(route.path.includes('/edit'));

const productId = Number(route.params.id);

const fetchProduct = async () => {
  try {
    loading.value = true;
    const response = await productApi.getProduct(productId);
    product.value = response.data;
  } catch (err) {
    error.value = 'Failed to load product';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProduct();
});

const updateProduct = async () => {
  if (!product.value) return;
  
  try {
    saving.value = true;
    const updateData: CreateProductDTO = {
      name: product.value.name,
      price: product.value.price,
      description: product.value.description,
      stock: product.value.stock
    };
    
    await productApi.updateProduct(productId, updateData);
    router.push('/products');
  } catch (err) {
    error.value = 'Failed to update product';
    console.error(err);
  } finally {
    saving.value = false;
  }
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
    <div v-if="loading" class="bg-white rounded-[12.75px] w-full max-w-[440px] mx-auto p-[24px] min-h-[200px] flex items-center justify-center">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-[#030213] border-t-transparent"></div>
    </div>

    <div v-else-if="error" class="bg-white rounded-[12.75px] w-full max-w-[440px] mx-auto p-[24px]">
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-[6.76px] text-[10.7px]">
        {{ error }}
      </div>
    </div>

    <div v-else-if="product" class="bg-white rounded-[12.75px] w-full max-w-[440px] mx-auto p-[24px] shadow-lg">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-[16px] text-[#0A0A0A] font-bold">{{ isEditMode ? 'Edit Product' : 'Product Details' }}</h1>
        <button 
          @click="router.push('/products')"
          class="text-[#717182] hover:text-black"
        >
          ✕
        </button>
      </div>
      
      <form @submit.prevent="updateProduct" class="space-y-4">
        <div>
          <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Product Name</label>
          <input
            v-model="product.name"
            type="text"
            required
            :disabled="!isEditMode"
            class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none disabled:bg-[#F3F3F5] disabled:opacity-90"
          />
        </div>

        <div>
          <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Description</label>
          <textarea
            v-model="product.description"
            rows="3"
            :disabled="!isEditMode"
            class="w-full px-3 py-2 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none min-h-[80px] disabled:bg-[#F3F3F5] disabled:opacity-90"
          ></textarea>
        </div>

        <div class="flex gap-4">
          <div class="w-1/2">
            <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Price ($)</label>
            <input
              v-model.number="product.price"
              type="number"
              step="0.01"
              required
              :disabled="!isEditMode"
              class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none disabled:bg-[#F3F3F5] disabled:opacity-90"
            />
          </div>

          <div class="w-1/2">
            <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Stock</label>
            <input
              v-model.number="product.stock"
              type="number"
              required
              :disabled="!isEditMode"
              class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none disabled:bg-[#F3F3F5] disabled:opacity-90"
            />
          </div>
        </div>

        <div class="flex justify-end space-x-3 pt-6 mt-2">
          <router-link
            to="/products"
            class="inline-flex items-center justify-center h-[36px] px-4 border border-black/10 rounded-md text-[12px] font-medium text-[#0A0A0A] hover:bg-black/5 transition-colors"
          >
            Cancel
          </router-link>
          <button
            v-if="isEditMode"
            type="submit"
            :disabled="saving"
            class="inline-flex items-center justify-center h-[36px] px-4 bg-[#030213] text-white rounded-md text-[12px] font-medium disabled:opacity-50"
          >
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
          <router-link
            v-if="!isEditMode"
            :to="`/products/${productId}/edit`"
            class="inline-flex items-center justify-center h-[36px] px-4 bg-[#030213] text-white rounded-md text-[12px] font-medium"
          >
            Edit
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
