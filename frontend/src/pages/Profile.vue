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
        <button @click="showPasswordModal = true" class="btn btn-outline-danger fw-bold">Change Password</button>
      </div>
    </div>

    <!-- Hobbies Section -->
    <div class="mt-5">
      <user-hobbies />
    </div>

    <!-- Password Update Modal -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <update-password @close="closePasswordModal"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import UpdatePassword from './UpdatePassword.vue';
import UserHobbies from './UpdateHobbies.vue';

function getCsrfToken(): string {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

interface Profile {
  username: string;
  name: string;
  email: string;
  date_of_birth: string;
}

export default defineComponent({
  name: 'Profile',

  components: {
    UpdatePassword,
    UserHobbies,
  },

  setup() {
    const profile = reactive<Profile>({
      username: '',
      name: '',
      email: '',
      date_of_birth: '',
    });

    const showPasswordModal = ref<boolean>(false);

    const closePasswordModal = (): void => {
      showPasswordModal.value = false;
    };

    const fetchProfile = async (): Promise<void> => {
      try {
        const response = await fetch('/api/profile', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data: Profile = await response.json();
          Object.assign(profile, data);
        } else {
          console.error('Failed to fetch profile data');
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    const updateProfile = async (): Promise<void>  => {
      try {
        const response = await fetch('/api/profile', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify(profile),
        });
        if (!response.ok) {
          console.error('Failed to update profile');
        } else {
          alert('Profile updated successfully');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    };

    fetchProfile();

    return {
      profile,
      updateProfile,
      showPasswordModal,
      closePasswordModal,
    };
  },
});
</script>

<style scoped>
  /* Define color variables */
  :root {
    --bg-color-light: #def2f1;
    --color-main: #2b7a78;
    --color-info: #3aafa9;
    --color-danger: #dc3545;
    --white: #fff;
  }

  /* Input and Label Styling */
  input {
    background-color: var(--bg-color-light);
    min-height: 50px;
  }

  label {
    font-size: large;
  }

  /* Background and Text Colors */
  .bg-main {
    background-color: var(--color-main) !important;
  }

  .text-main {
    color: var(--color-main) !important;
  }

  /* Button Styles */
  

  .btn-outline-danger {
    color: var(--color-danger);
    border-color: var(--color-danger);
    transition: background-color 0.3s, color 0.3s;
  }

  .btn-outline-danger:hover {
    background-color: var(--color-danger);
    color: var(--white);
  }

  /* Utility Classes */
  .rounded-lg {
    border-radius: 0.5rem;
  }

  .shadow-lg {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  /* Modal Overlay and Content */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }

  .modal-content {
    background-color: var(--white);
    padding: 20px;
    border-radius: 8px;
    max-width: 500px;
    width: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
</style>

