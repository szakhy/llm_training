
<template>
  <div class="fixed bottom-4 left-4 bg-white shadow-lg rounded-lg p-4 w-80 z-50">
    <h3 class="font-bold mb-2">Shopping Cart</h3>
    <div v-if="cart.items.length === 0" class="text-gray-500">Cart is empty</div>
    <ul v-else>
      <li v-for="item in cart.items" :key="item.id" class="flex justify-between items-center mb-2">
        <div class="flex flex-col w-40">
          <span class="truncate">{{ item.product.name }}</span>
          <span class="text-xs text-gray-400">Stock: {{ item.product.stock }}</span>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="updateQuantity(item, item.quantity - 1)"
            :disabled="item.quantity <= 1 || loading"
            class="w-6 h-6 flex items-center justify-center rounded bg-yellow-200 hover:bg-yellow-300 text-yellow-900 disabled:opacity-50 border border-yellow-300"
            title="Decrease quantity"
          >
            -
          </button>
          <span class="w-6 text-center">{{ item.quantity }}</span>
          <button
            @click="updateQuantity(item, item.quantity + 1)"
            :disabled="item.quantity >= item.product.stock || loading"
            class="w-6 h-6 flex items-center justify-center rounded bg-blue-200 hover:bg-blue-300 text-blue-900 disabled:opacity-50 border border-blue-300"
            title="Increase quantity"
          >
            +
          </button>
        </div>
        <span class="text-sm text-gray-600 w-16 text-right">${{ (item.product.price * item.quantity).toFixed(2) }}</span>
        <button
          @click="removeItem(item)"
          :disabled="loading"
          class="ml-2 w-6 h-6 flex items-center justify-center rounded bg-red-200 hover:bg-red-400 text-red-700 disabled:opacity-50 border border-red-300"
          title="Remove from cart"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
  </li>
    </ul>
    <div v-if="cart.items.length > 0" class="mt-2 font-semibold">
      Total: ${{ totalPrice.toFixed(2) }}
    </div>
  <div v-if="error" class="text-xs text-red-500 mt-2">{{ error }}</div>
  <!-- Remove accidental code output below -->
  </div>
</template>


<script setup lang="ts">
import { computed, defineProps, ref } from 'vue';
import { cartApi, type CartDTO, type CartItemDTO } from '../api';

const props = defineProps<{ cart: CartDTO }>();
const emit = defineEmits(['cart-updated']);

const loading = ref(false);
const error = ref('');

const totalPrice = computed(() =>
  props.cart.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0)
);

async function updateQuantity(item: CartItemDTO, newQty: number) {
  if (newQty < 1 || newQty > item.product.stock) return;
  loading.value = true;
  error.value = '';
  try {
    const response = await cartApi.updateQuantity({ product_id: item.product.id, quantity: newQty });
    emit('cart-updated', response.data);
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to update cart';
  } finally {
    loading.value = false;
  }
}

async function removeItem(item: CartItemDTO) {
  loading.value = true;
  error.value = '';
  try {
    const response = await cartApi.removeItem({ product_id: item.product.id, quantity: item.quantity });
    emit('cart-updated', response.data);
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to remove item';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.fixed {
  box-shadow: 0 2px 16px rgba(0,0,0,0.12);
}
</style>
