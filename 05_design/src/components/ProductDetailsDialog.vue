<!-- 
  ProductDetailsDialog.vue
  
  This component is based on the Figma design and shows product details in a dialog
  instead of navigating to a separate page.
-->

<template>
  <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-30" @click="$emit('close')"></div>
    
    <!-- Dialog based on Figma design -->
    <div class="bg-white rounded-[8.75px] w-full max-w-[444px] mx-auto z-10 relative border border-black/10 shadow-[0px_10px_15px_0px_rgba(0,0,0,0.1),0px_4px_6px_0px_rgba(0,0,0,0.1)]">
      <div class="p-[22px] relative">
        <!-- Header -->
        <div>
          <h3 class="text-base font-semibold text-black leading-[0.984375em] mt-[21px]">Product Details</h3>
        </div>
        
        <!-- Close button (X) -->
        <button 
          @click="$emit('close')" 
          class="absolute top-[15px] right-[15px] w-6 h-6 flex items-center justify-center"
        >
          <svg width="12" height="12" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
            <line x1="1" y1="1" x2="11" y2="11" stroke="black" stroke-width="2" />
            <line x1="1" y1="11" x2="11" y2="1" stroke="black" stroke-width="2" />
          </svg>
        </button>
        
        <!-- Product name -->
        <h2 class="text-base font-medium text-black mt-[10px] leading-[1.4765625em]">{{ product.name }}</h2>
        
        <!-- Product description -->
        <p class="text-base text-[#717182] leading-[1.5em] mt-[9px]">{{ product.description || 'No description available' }}</p>
        
        <!-- Separator line -->
        <div class="h-px w-full bg-black/10 mt-[11px] mb-[15px]"></div>
        
        <!-- Price and Stock information -->
        <div class="flex justify-between mb-[10px]">
          <!-- Price (left side) -->
          <div>
            <p class="text-xs text-[#717182]">Price:</p>
            <p class="text-xs font-medium text-[#030213]">${{ product.price.toFixed(2) }}</p>
          </div>
          
          <!-- Stock (right side) -->
          <div class="mr-[150px]">
            <p class="text-xs text-[#717182]">Stock:</p>
            <p class="text-xs text-black">{{ product.stock }} units</p>
          </div>
        </div>
        
        <!-- Product ID (below price and stock but closer) -->
        <div>
          <p class="text-xs text-[#717182]">Product ID:</p>
          <p class="text-[11px] text-black">{{ product.id }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '../api';

defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  product: {
    type: Object as () => Product,
    required: true
  }
});

defineEmits(['close']);
</script>
