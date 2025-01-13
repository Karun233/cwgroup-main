<template>
    <div class="container mt-5">
      <h1>Similar Users</h1>
  
      <!-- Filters -->
      <div class="filters mb-4">
        <label>
          <span>Min Age: </span>
          <input
            type="number"
            v-model="state.filters.ageMin"
            @change="applyFilters"
            placeholder="No minimum"
            class="form-control d-inline-block"
            style="width: 120px;"
          />
        </label>
        <label class="ms-3">
          <span>Max Age: </span>
          <input
            type="number"
            v-model="state.filters.ageMax"
            @change="applyFilters"
            placeholder="No maximum"
            class="form-control d-inline-block"
            style="width: 120px;"
          />
        </label>
      </div>
  
  
      <!-- Users List -->
      <ul class="list-group" v-if="state.users.length > 0">
        <li
          v-for="user in state.users"
          :key="user.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <div>
            <strong>{{ user.name }}</strong>
            <span>(Age: {{ user.age }})</span>
          </div>
          <div>
            Common Hobbies: <strong>{{ user.common_hobbies }}</strong>
          </div>
        </li>
      </ul>
  
      <!-- No Results -->
      <p v-else class="text-muted mt-3">
        No similar users found.
      </p>
  
      <!-- Pagination Controls -->
      <div
        class="pagination mt-4 d-flex justify-content-center align-items-center gap-3"
        v-if="state.totalPages > 1"
      >
        <button
          class="btn btn-outline-primary"
          @click="prevPage"
          :disabled="state.page <= 1"
        >
          Previous
        </button>
        <span>Page {{ state.page }} of {{ state.totalPages }}</span>
        <button
          class="btn btn-outline-primary"
          @click="nextPage"
          :disabled="state.page >= state.totalPages"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from "vue";
  
  interface User {
    id: number;
    name: string;
    age: number | null;
    common_hobbies: number;
  }
  
  export default defineComponent({
    name: "CommonHobbies",
    setup() {
      // Create a reactive state object
      const state = reactive({
        users: [] as User[],
        page: 1,
        totalPages: 1,
        filters: {
          ageMin: "", // No minimum age by default
          ageMax: "", // No maximum age by default
        },
      });
  
      const fetchUsers = async () => {
        const params = new URLSearchParams();
  
        // Add pagination
        params.append("page", state.page.toString());
  
        // Add filters if they exist
        if (state.filters.ageMin) params.append("age_min", state.filters.ageMin);
        if (state.filters.ageMax) params.append("age_max", state.filters.ageMax);
  
        try {
          const response = await fetch(`/api/similar-hobbies/?${params.toString()}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include", // if your Django CSRF/cookie setup needs it
          });
  
          if (!response.ok) {
            console.error(`API Error: ${response.status}`);
            return;
          }
  
          // Parse JSON
          const data = await response.json();
          console.log("API Response:", data);
  
          // Assign to state
          state.users = Array.isArray(data.users) ? data.users : [];
          state.page = data.page || 1;
          state.totalPages = data.pages || 1;
  
        } catch (error) {
          console.error("Error fetching similar users:", error);
        }
      };
  
      const prevPage = () => {
        if (state.page > 1) {
          state.page--;
          fetchUsers();
        }
      };
  
      const nextPage = () => {
        if (state.page < state.totalPages) {
          state.page++;
          fetchUsers();
        }
      };
  
      const applyFilters = () => {
        state.page = 1;
        fetchUsers();
      };
  
      // Fetch initial data on component mount
      fetchUsers();
  
      // Return state object and methods so they are accessible in the template
      return {
        state,
        fetchUsers,
        prevPage,
        nextPage,
        applyFilters,
      };
    },
  });
  </script>
  
  <style scoped>
  /* Optional: simple styling, no changes needed */
  </style>
  