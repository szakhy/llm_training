<template>
  <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-30" @click="$emit('close')"></div>
    
    <!-- Modal -->
    <div class="bg-white rounded-[12.75px] w-full max-w-[380px] mx-auto z-10 relative overflow-hidden">
      <div class="p-5">
        <div class="text-center mb-6">
          <h3 class="text-[16px] font-medium text-[#0A0A0A]">{{ title }}</h3>
          <p class="mt-3 text-[13.2px] text-[#717182]">{{ message }}</p>
        </div>
        
        <div class="flex justify-center gap-3 mt-6">
          <button 
            @click="$emit('close')" 
            class="px-5 py-[9px] border border-black/10 text-[#0A0A0A] rounded-[6.76px] text-[11.3px] font-medium hover:bg-gray-100 focus:outline-none"
          >
            {{ cancelText }}
          </button>
          <button 
            @click="$emit('confirm')" 
            class="px-5 py-[9px] bg-[#D4183D] text-white rounded-[6.76px] text-[11.3px] font-medium hover:bg-[#BD1636] focus:outline-none"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirmation'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  }
});

defineEmits(['close', 'confirm']);
</script>
