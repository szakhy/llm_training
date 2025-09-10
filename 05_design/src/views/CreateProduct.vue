<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { productApi, type CreateProductDTO } from '../api';

const router = useRouter();
const error = ref<string | null>(null);
const saving = ref(false);

const newProduct = ref<CreateProductDTO>({
  name: '',
  price: 0,
  description: '',
  stock: 0
});

const createProduct = async () => {
  try {
    saving.value = true;
    await productApi.createProduct(newProduct.value);
    router.push('/products');
  } catch (err) {
    error.value = 'Failed to create product';
    console.error(err);
  } finally {
    saving.value = false;
  }
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
    <div class="bg-white rounded-[12.75px] w-full max-w-[440px] mx-auto p-[24px] shadow-lg">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-[16px] text-[#0A0A0A] font-bold">Add New Product</h1>
        <button 
          @click="router.push('/products')"
          class="text-[#717182] hover:text-black"
        >
          ✕
        </button>
      </div>

      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-[6.76px] mb-4 text-[10.7px]">
        {{ error }}
      </div>
      
      <form @submit.prevent="createProduct" class="space-y-4">
        <div>
          <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Product Name</label>
          <input
            v-model="newProduct.name"
            type="text"
            placeholder="Enter product name"
            required
            class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-[6.76px] text-[12px] text-[#0A0A0A] focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Description</label>
          <textarea
            v-model="newProduct.description"
            rows="3"
            placeholder="Enter product description"
            class="w-full px-3 py-2 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none min-h-[80px]"
          ></textarea>
        </div>

        <div class="flex gap-4">
          <div class="w-1/2">
            <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Price ($)</label>
            <input
              v-model.number="newProduct.price"
              type="number"
              step="0.01"
              placeholder="0.00"
              required
              class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none"
            />
          </div>

          <div class="w-1/2">
            <label class="block text-[12px] font-medium text-[#0A0A0A] mb-[8px]">Stock</label>
            <input
              v-model.number="newProduct.stock"
              type="number"
              placeholder="0"
              required
              class="w-full h-[36px] px-3 bg-[#F3F3F5] rounded-md text-[12px] text-[#0A0A0A] focus:outline-none"
            />
          </div>
        </div>

        <div class="flex justify-end space-x-3 pt-6 mt-2">
          <button
            type="button"
            @click="router.push('/products')"
            class="inline-flex items-center justify-center h-[36px] px-4 border border-black/10 rounded-md text-[12px] font-medium text-[#0A0A0A] hover:bg-black/5 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="inline-flex items-center justify-center h-[36px] px-4 bg-[#030213] text-white rounded-md text-[12px] font-medium disabled:opacity-50"
          >
            {{ saving ? 'Adding...' : 'Add Product' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
