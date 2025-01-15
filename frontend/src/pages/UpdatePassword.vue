<template>
  <div class="container mt-5" style="background-color: white; border-radius: 8px; padding: 30px;">
    <h1 class="mb-4" style="color: #17252A;">Change Password</h1>
    <form @submit.prevent="submitForm" class="needs-validation" novalidate>

      <div class="mb-3">
        <label for="current_password" class="form-label" style="color: #17252A;">Current Password</label>
        <div class="input-group">
          <input
            :type="showCurrentPassword ? 'text' : 'password'"
            id="current_password"
            v-model="currentPassword"
            class="form-control"
            required
            style="background-color: #feffff; border: 1px solid #2b7a78; color: #17252A;"
          />
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="toggleShowCurrentPassword"
            style="background-color: #0dcaf0; color: #feffff; border: none;"
          >
            <i class="bi" :class="showCurrentPassword ? 'bi-eye' : 'bi-eye-slash'"></i>
          </button>
        </div>
      </div>

      <div class="mb-3">
        <label for="new_password" class="form-label" style="color: #17252A;">New Password</label>
        <div class="input-group">
          <input
            :type="showNewPassword ? 'text' : 'password'"
            id="new_password"
            v-model="newPassword"
            @input="checkPasswordRequirements"
            class="form-control"
            required
            style="background-color: #feffff; border: 1px solid #2b7a78; color: #17252A;"
          />

          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="toggleShowNewPassword"
            style="background-color: #0dcaf0; color: #feffff; border: none;"
          >
            <i class="bi" :class="showCurrentPassword ? 'bi-eye' : 'bi-eye-slash'"></i>
          </button>
        </div>

        <ul class="mt-3" style="list-style-type: none; padding-left: 0;">
          <li
            :style="{ color: passwordRequirements.length ? 'green' : 'red' }"
          >
            Minimum 8 characters
          </li>
          <li
            :style="{ color: passwordRequirements.nonNumeric ? 'green' : 'red' }"
          >
            Password should not be entirely numeric
          </li>
        </ul>
      </div>

      <div class="mb-3">
        <label for="confirm_password" class="form-label" style="color: #17252A;">Confirm New Password</label>
        <div class="input-group">
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            id="confirm_password"
            v-model="confirmPassword"
            class="form-control"
            required
            style="background-color: #feffff; border: 1px solid #2b7a78; color: #17252A;"
          />
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="toggleShowConfirmPassword"
            style="background-color: #0dcaf0; color: #feffff; border: none;"
          >
            <i class="bi" :class="showCurrentPassword ? 'bi-eye' : 'bi-eye-slash'"></i>
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="alert alert-danger" role="alert" style="background-color: #ff6b6b; color: #feffff;">
        {{ errorMessage }}
      </div>

      <div class="text-center">
        <button type="submit" class="btn" style="background-color: #0dcaf0; color: #feffff; border: none;">Update Password</button>
        <button type="button" class="btn btn-outline-danger" @click="closeModal">Cancel</button>
      </div>
      
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ChangePassword',
  setup(_, {emit}) {

    const currentPassword = ref<string>('');
    const newPassword = ref<string>('');
    const confirmPassword = ref<string>('');
    const errorMessage = ref<string>('');

    const showCurrentPassword = ref<boolean>(false);
    const showNewPassword = ref<boolean>(false);
    const showConfirmPassword = ref<boolean>(false);

    const closeModal = () => {
      emit('close');
    };

    const toggleShowCurrentPassword = () => {
      showCurrentPassword.value = !showCurrentPassword.value;
    };

    const toggleShowNewPassword = () => {
      showNewPassword.value = !showNewPassword.value;
    };

    const toggleShowConfirmPassword = () => {
      showConfirmPassword.value = !showConfirmPassword.value;
    };

    const passwordRequirements = ref({
      length: false,
      nonNumeric: false,
    });

    const checkPasswordRequirements = (): void => {
      const password = newPassword.value;
      passwordRequirements.value.length = password.length >= 8;
      passwordRequirements.value.nonNumeric = !/^\d+$/.test(password) && /[a-zA-Z!@#$%^&*(),.?":{}|<>]/.test(password); 
    };

    const submitForm = async (): Promise<void> => {
      if (newPassword.value !== confirmPassword.value) {
        errorMessage.value = 'Passwords do not match!';
        return;
      }

      try {
        const response = await fetch('/api/update-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), 
          },
          body: JSON.stringify({
            current_password: currentPassword.value,
            new_password: newPassword.value,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          errorMessage.value = data.error || 'An error occurred.';
        } else {
          
          alert('Password changed successfully!');
          
        }
      } catch (error) {
        errorMessage.value = 'An error occurred. Please try again.';
      }
    };

    const getCSRFToken = (): string => {
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      return match ? match[1] : '';
    };

    return {
      currentPassword,
      newPassword,
      confirmPassword,
      errorMessage,
      passwordRequirements,
      submitForm,
      checkPasswordRequirements,
      showCurrentPassword,
      showNewPassword,
      showConfirmPassword,
      toggleShowCurrentPassword,
      toggleShowNewPassword,
      toggleShowConfirmPassword,
      closeModal,
    };
  },
});
</script>

<style scoped>
.error {
  color: red;
}
</style>