<template>
  <button 
    @click="onClick"
    :disabled="disabled"
    :class="[
      'px-4 py-2 rounded-md font-medium text-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
      disabled ? 'opacity-50 cursor-not-allowed' : 'hover:transform hover:scale-105',
      variant === 'primary' ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500' :
      variant === 'secondary' ? 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500' :
      variant === 'success' ? 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500' :
      variant === 'danger' ? 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500' :
      variant === 'warning' ? 'bg-yellow-500 text-white hover:bg-yellow-600 focus:ring-yellow-400' :
      variant === 'outline' ? 'border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white focus:ring-blue-500' :
      'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'
    ]"
  >
    <slot>{{ text }}</slot>
  </button>
</template>

<script setup>
defineProps({
  onClick: {
    type: Function,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'outline'].includes(value)
  },
  text: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
/* Generic Button Styles */
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.rounded-md { border-radius: 0.375rem; }
.font-medium { font-weight: 500; }
.text-sm { font-size: 1rem; line-height: 1.25rem; }
.transition-all { transition-property: all; }
.duration-200 { transition-duration: 200ms; }
.focus\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; }
.focus\:ring-2:focus { box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000); --tw-ring-offset-width: 0px; --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color); }
.focus\:ring-offset-2:focus { --tw-ring-offset-width: 2px; }

/* Colors */
.bg-blue-600 { background-color: #2563eb; }
.bg-blue-700 { background-color: #1d4ed8; }
.bg-gray-600 { background-color: #4b5563; }
.bg-gray-700 { background-color: #374151; }
.bg-green-600 { background-color: #16a34a; }
.bg-green-700 { background-color: #15803d; }
.bg-red-600 { background-color: #dc2626; }
.bg-red-700 { background-color: #b91c1c; }
.bg-yellow-500 { background-color: #eab308; }
.bg-yellow-600 { background-color: #ca8a04; }
.text-white { color: #ffffff; }
.text-blue-600 { color: #2563eb; }
.border-2 { border-width: 2px; }
.border-blue-600 { border-color: #2563eb; }

/* Hover effects */
.hover\:bg-blue-700:hover { background-color: #1d4ed8; }
.hover\:bg-gray-700:hover { background-color: #374151; }
.hover\:bg-green-700:hover { background-color: #15803d; }
.hover\:bg-red-700:hover { background-color: #b91c1c; }
.hover\:bg-yellow-600:hover { background-color: #ca8a04; }
.hover\:bg-blue-600:hover { background-color: #2563eb; }
.hover\:text-white:hover { color: #ffffff; }
.hover\:transform:hover { transform: translateX(var(--tw-translate-x)) translateY(var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y)); }
.hover\:scale-105:hover { --tw-scale-x: 1.05; --tw-scale-y: 1.05; }

/* Focus ring colors */
.focus\:ring-blue-500:focus { --tw-ring-color: #3b82f6; }
.focus\:ring-gray-500:focus { --tw-ring-color: #6b7280; }
.focus\:ring-green-500:focus { --tw-ring-color: #22c55e; }
.focus\:ring-red-500:focus { --tw-ring-color: #ef4444; }
.focus\:ring-yellow-400:focus { --tw-ring-color: #facc15; }

/* Disabled states */
.opacity-50 { opacity: 0.5; }
.cursor-not-allowed { cursor: not-allowed; }

/* Button reset */
button {
  box-shadow: 2px 2px gray;
  border: none;
  cursor: pointer;
  font-family: inherit;
}
</style>

<!-- .smc-note p{
  padding: 0px;
  font-size: x-small;
  align-self: auto;
  margin: 0px;
}

.custom-title{
  margin-bottom: 0px;
}
<div class="">
  <h3 class="text-lg font-semibold text-gray-800 custom-title">Custom Spell Material Components</h3>
  <div class="smc-note flex">
    <p class="px-6 py-3 text-left text-xs text-gray-500">(Expected custom item naming format: "SMC:Diamond_Dust:500GP")</p>
  </div>
</div>
<svg class="w-5 h-5 alight-right" :class="{ 'transform rotate-90': showCustomItems }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
</svg>
          </button> -->