<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { productApi, type Product } from '../api';
import ConfirmDialog from '../components/ConfirmDialog.vue';
import ProductDetailsDialog from '../components/ProductDetailsDialog.vue';

const products = ref<Product[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const searchQuery = ref('');
const showDeleteConfirm = ref(false);
const productToDelete = ref<number | null>(null);
const showProductDetails = ref(false);
const selectedProduct = ref<Product | null>(null);

const fetchProducts = async () => {
  try {
    loading.value = true;
    const response = await productApi.getProducts();
    products.value = response.data;
  } catch (err: any) {
    error.value = `Failed to load products: ${err.message}`;
    console.error('API Error:', err.response?.data || err.message);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProducts();
});

const confirmDelete = (id: number) => {
  productToDelete.value = id;
  showDeleteConfirm.value = true;
};

const viewProductDetails = (product: Product) => {
  selectedProduct.value = product;
  showProductDetails.value = true;
};

const deleteProduct = async () => {
  if (!productToDelete.value) return;
  
  try {
    await productApi.deleteProduct(productToDelete.value);
    products.value = products.value.filter(p => p.id !== productToDelete.value);
    showDeleteConfirm.value = false;
    productToDelete.value = null;
  } catch (err) {
    error.value = 'Failed to delete product';
    console.error(err);
  }
};

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value;
  const query = searchQuery.value.toLowerCase();
  return products.value.filter(product => 
    product.name.toLowerCase().includes(query) || 
    (product.description ? product.description.toLowerCase().includes(query) : false)
  );
});

// Function to truncate text to a specific length and add ellipsis
const truncateText = (text, maxLength = 100) => {
  if (!text) return 'No description available';
  return text.length > maxLength ? text.slice(0, maxLength) + '...' : text;
};
</script>

<template>
  <div class="max-w-7xl mx-auto py-5">
    <div class="w-[calc(260px*4+1.5rem*3)] mx-auto px-0">
      <h1 class="text-[18px] text-[#0A0A0A] font-medium mb-6">Product Management</h1>

      <div class="mb-6 flex justify-between items-center">
        <div class="relative w-[392.35px]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search products..."
            class="w-full h-[31.53px] pl-[40px] pr-4 bg-[#F3F3F5] rounded-[6.76px] text-[10.7px] text-[#0A0A0A] focus:outline-none"
          />
          <div class="absolute left-[13.76px] top-[9.76px] w-[24px] h-[14px]">
            <img src="../assets/icons/search-icon.svg" class="w-full h-full" alt="Search" />
          </div>
        </div>

        <router-link
          to="/products/create"
          class="inline-flex items-center gap-2 h-[31.53px] px-4 bg-[#030213] text-white rounded-[6.76px] text-[11.3px] font-medium"
        >
          <div class="flex items-center justify-center">
            <img src="../assets/icons/add-icon.svg" alt="+" class="w-[14px] h-[14px]" />
          </div>
          <span>Add Product</span>
        </router-link>
      </div>

      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-[#030213] border-t-transparent mx-auto"></div>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-[12.75px]">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          class="bg-white rounded-[12.75px] border border-black/10 w-[260px] h-[240px] flex flex-col overflow-hidden"
        >
          <!-- Product content section - growing to fill space -->
          <div class="px-[15px] pt-[15px] flex-1 flex flex-col">
            <!-- Product title - fixed line height to prevent cut-off -->
            <h4 class="text-[13.2px] text-[#0A0A0A] font-normal leading-[1.3] mb-[14px] truncate">
              {{ product.name }}
            </h4>

            <!-- Product description - takes remaining space with truncation -->
            <div class="flex-1 overflow-hidden">
              <p class="text-[11.3px] text-[#717182] leading-[1.55] line-clamp-3 overflow-hidden" style="display: -webkit-box; -webkit-box-orient: vertical;">
                {{ truncateText(product.description, 100) }}
              </p>
            </div>

            <!-- Price and stock info -->
            <div class="flex justify-between items-center mb-[20px]">
              <span class="text-[12.8px] text-[#030213] font-medium">${{ product.price.toFixed(2) }}</span>
              <span class="text-[11.3px] text-[#717182]">Stock: {{ product.stock }}</span>
            </div>
            
            <!-- Action buttons positioned at bottom middle -->
            <div class="flex items-center justify-center gap-[7px] pb-[14px]">
              <button
                @click="viewProductDetails(product)"
                class="inline-flex items-center justify-center gap-2 h-7 min-w-[85px] px-4 border border-black/10 rounded-[6.75px] text-[11.3px] font-medium text-[#0A0A0A] hover:bg-black/5 transition-colors"
              >
                <img src="../assets/icons/view-icon.svg" alt="View" class="w-[14px] h-[14px]" />
                <span>View</span>
              </button>

              <router-link
                :to="`/products/${product.id}/edit`"
                class="inline-flex items-center justify-center gap-2 h-7 min-w-[85px] px-4 border border-black/10 rounded-[6.75px] text-[11.3px] font-medium text-[#0A0A0A] hover:bg-black/5 transition-colors"
              >
                <img src="../assets/icons/edit-icon.svg" alt="Edit" class="w-[14px] h-[14px]" />
                <span>Edit</span>
              </router-link>

              <button
                @click="confirmDelete(product.id)"
                class="inline-flex items-center justify-center w-[31.5px] h-7 bg-[#D4183D] rounded-[6.75px] hover:bg-[#BD1636] transition-colors"
              >
                <img src="../assets/icons/delete-icon.svg" alt="Delete" class="w-[14px] h-[14px]" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Delete Confirmation Modal -->
      <ConfirmDialog
        :is-open="showDeleteConfirm"
        title="Delete Product"
        message="Are you sure you want to delete this product? This action cannot be undone."
        confirm-text="Delete"
        cancel-text="Cancel"
        @close="showDeleteConfirm = false"
        @confirm="deleteProduct"
      />
      
      <!-- Product Details Dialog -->
      <ProductDetailsDialog
        v-if="selectedProduct"
        :is-open="showProductDetails"
        :product="selectedProduct"
        @close="showProductDetails = false"
      />
    </div>
  </div>
</template>
