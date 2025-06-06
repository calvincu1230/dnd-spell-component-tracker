<template>
  <div v-if="props.show" class="modal-overlay" @click="handleCancel">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">{{ props.title || 'Confirm Action' }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ props.message }}</p>
      </div>
      <div class="modal-footer">
        <GenericButton 
          :onClick="handleCancel"
          :text="cancelText || 'Cancel'"
          variant="outline"
        />
        <GenericButton 
          :onClick="handleConfirm"
          :text="confirmText || 'Confirm'"
          :variant="confirmVariant || 'danger'"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import GenericButton from './buttons/GenericButton.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmVariant: {
    type: String,
    default: 'danger'
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  max-width: 400px;
  width: 90%;
  animation: modalAppear 0.2s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.modal-body {
  padding: 1rem 1.5rem;
  color: #4b5563;
  line-height: 1.5;
}

.modal-footer {
  padding: 0 1.5rem 1.5rem 1.5rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

/* Responsive Design */
@media (max-width: 640px) {
  .modal-content {
    margin: 1rem;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
  }
}
</style>