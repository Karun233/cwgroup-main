<template>
  <div class="hobbies-list container bg-def2f1 p-4 rounded">
    <h1 class="text-center text-3aafa9 mb-4">Update Hobbies</h1>

    <!-- Section for selecting or adding a hobby -->
    <h2 class="text-17252A mb-3">Add Hobbies</h2>
    <div class="mb-3">
      <label for="allHobbies" class="form-label text-17252A"></label>
      <select
        id="allHobbies"
        v-model="selectedHobbyId"
        class="form-select border-2b7a78"
      >
        <option value="">--Select a hobby--</option>
        <option v-for="hobby in allHobbies" :key="hobby.id" :value="hobby.id">
          {{ hobby.name }}
        </option>
        <option value="other">+Add A New Hobby</option>
      </select>

      <div v-if="message" class="alert alert-success mt-3" role="alert">
        {{ message }}
      </div>
    </div>

    <div v-if="selectedHobbyId === 'other'" class="mb-3">
      <input
        type="text"
        v-model="newHobbyName"
        placeholder="Enter your new hobby"
        class="form-control border-2b7a78"
      />
    </div>

    <button
      @click="addHobby"
      class="btn btn-3aafa9 text-feffff w-100 mb-4"
      :disabled="!selectedHobbyId || (selectedHobbyId === 'other' && !newHobbyName)"
    >
      Add Hobby
    </button>

    <!-- Section for displaying user's hobbies -->
    <h2 class="text-17252A mb-3">Added Hobbies</h2>
    <ul v-if="hobbies.length > 0" class="list-group">
      <li
        v-for="hobby in hobbies"
        :key="hobby.id"
        class="list-group-item d-flex justify-content-between align-items-center bg-def2f1 text-17252A border-2b7a78"
      >
        {{ hobby.name }}
        <button
          @click="confirmDelete(hobby.id, hobby.name)"
          class="btn btn-danger btn-sm"
        >
          <i class="bi bi-trash"></i>
        </button>
      </li>
    </ul>
    <p v-else class="text-center text-2b7a78">
      No Hobbies Added
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { storeToRefs } from 'pinia';                 // <-- import storeToRefs
import { useHobbyStore } from '../stores/useHobbyStore';

export default defineComponent({
  name: 'UserHobbies',
  setup() {
    const hobbyStore = useHobbyStore();

    // Convert store properties to refs so they're fully reactive
    const {
      hobbies,
      allHobbies,
      selectedHobbyId,
      newHobbyName,
      message
    } = storeToRefs(hobbyStore);

    // Lifecycle
    onMounted(() => {
      hobbyStore.fetchHobbies();
      hobbyStore.fetchAllHobbies();
    });

    return {
      // Reactive state
      hobbies,
      allHobbies,
      selectedHobbyId,
      newHobbyName,
      message,

      // Actions
      addHobby: hobbyStore.addHobby,
      confirmDelete: hobbyStore.confirmDelete,
    };
  },
});
</script>
