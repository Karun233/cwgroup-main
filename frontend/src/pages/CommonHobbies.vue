<template>
    <div>
      <h1>Similar Users</h1>
      
      <!-- Filters -->
      <div class="filters">
        <label>
          Age Min:
          <input type="number" v-model="filters.ageMin" @change="fetchUsers" />
        </label>
        <label>
          Age Max:
          <input type="number" v-model="filters.ageMax" @change="fetchUsers" />
        </label>
      </div>
  
      <!-- Users List -->
      <ul>
        <li v-for="user in users" :key="user.id">
          {{ user.name }} ({{ user.age }} years old) - Common Hobbies: {{ user.common_hobbies }}
        </li>
      </ul>
  
      <!-- Pagination -->
      <div class="pagination">
        <button @click="prevPage" :disabled="page <= 1">Previous</button>
        <span>Page {{ page }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="page >= totalPages">Next</button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from "vue";

// Define the interface for a user
interface User {
  id: number;
  name: string;
  age: number;
  common_hobbies: number;
}

export default defineComponent({
  name: "UsersPage",
  setup() {
    const state = reactive<{
      users: User[]; // Explicitly define 'users' as an array of User
      page: number;
      totalPages: number;
      filters: {
        ageMin: number;
        ageMax: number;
      };
    }>({
      users: [], // Initialize as an empty array of users
      page: 1,
      totalPages: 1,
      filters: {
        ageMin: 0,
        ageMax: 150,
      },
    });

    const fetchUsers = async () => {
      const params = new URLSearchParams({
        age_min: state.filters.ageMin.toString(),
        age_max: state.filters.ageMax.toString(),
        page: state.page.toString(),
      });

      try {
        const response = await fetch(`/api/similar-users/?${params}`);
        const data = await response.json();
        state.users = data.users;
        state.page = data.page;
        state.totalPages = data.pages;
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    };

    const prevPage = () => {
      if (state.page > 1) {
        state.page -= 1;
        fetchUsers();
      }
    };

    const nextPage = () => {
      if (state.page < state.totalPages) {
        state.page += 1;
        fetchUsers();
      }
    };

    // Fetch users on mount
    fetchUsers();

    return { ...state, fetchUsers, prevPage, nextPage };
        },
    });