<template>
  <div class="container py-5">
    <!-- Profile Form -->
    <div class="box p-5 rounded-lg shadow-lg">
      <form @submit.prevent="updateProfile">
        <!-- Username Field -->
        <div class="mb-4">
          <label for="username" class="form-label fw-bold text-main">Username:</label>
          <input
            id="username"
            type="text"
            class="form-control"
            v-model="profile.username"
            :disabled="false"
          />
        </div>

        <!-- Name Field -->
        <div class="mb-4">
          <label for="name" class="form-label fw-bold text-main">Name:</label>
          <input
            id="name"
            type="text"
            class="form-control"
            v-model="profile.name"
          />
        </div>

        <!-- Email Field -->
        <div class="mb-4">
          <label for="email" class="form-label fw-bold text-main">Email:</label>
          <input
            id="email"
            type="email"
            class="form-control"
            v-model="profile.email"
          />
        </div>

        <!-- Date of Birth Field -->
        <div class="mb-4">
          <label for="date_of_birth" class="form-label fw-bold text-main">Date of Birth:</label>
          <input
            id="date_of_birth"
            type="date"
            class="form-control"
            v-model="profile.date_of_birth"
          />
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button type="submit" class="btn btn-info text-white fw-bold">Update Profile</button>
        </div>
      </form>

      <div class="mt-4 d-flex justify-content-center gap-3">
        <!-- Change Password Button (Triggers Modal) -->
        <button @click="showPasswordModal = true" class="btn btn-outline-danger fw-bold">
          Change Password
        </button>
      </div>
    </div>

    <!-- Hobbies Section -->
    <div class="mt-5">
      <user-hobbies />
    </div>

    <!-- Password Update Modal -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <update-password @close="closePasswordModal" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';            // <-- Import storeToRefs
import UpdatePassword from './UpdatePassword.vue';
import UserHobbies from './UpdateHobbies.vue';
import { useUserStore } from '../stores/useUserStore';

export default defineComponent({
  name: 'Profile',
  components: {
    UpdatePassword,
    UserHobbies,
  },
  setup() {
    const userStore = useUserStore();
    // De-structure reactive refs using storeToRefs
    // This ensures `profile` remains fully reactive 
    // when userStore.profile changes.
    const { profile } = storeToRefs(userStore);

    const showPasswordModal = ref(false);
    const closePasswordModal = () => {
      showPasswordModal.value = false;
    };

    // Load the current profile from the store
    onMounted(() => {
      userStore.fetchProfile();
    });

    // Invokes the store action to update the profile
    const updateProfile = async () => {
      await userStore.updateProfile();
      // userStore.updateProfile() re-fetches the profile,
      // so `profile` in the store should be updated automatically
      // thanks to storeToRefs.
    };

    return {
      profile,            // now a ref, so template usage is fully reactive
      updateProfile,
      showPasswordModal,
      closePasswordModal,
    };
  },
});
</script>