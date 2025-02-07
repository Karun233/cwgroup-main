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

        <div v-if="Message" class="alert alert-success mt-3" role="alert">
          {{ Message }}
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
            @click="confirmDelete(hobby)"
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
    import { defineComponent, ref, onMounted } from 'vue';
  
    interface Hobby {
      id: number;
      name: string;
    }
  
    export default defineComponent({
      name: "UserHobbies",
      setup() {
        const hobbies = ref<Hobby[]>([]);
        const allHobbies = ref<Hobby[]>([]);
        const selectedHobbyId = ref<string | null>('');
        const newHobbyName = ref<string>('');
        const Message = ref<string | null>(null);
  
        const fetchHobbies = async () => {
          try {
            const response = await fetch("/api/hobbies/");
            if (!response.ok) {
              throw new Error("Failed to fetch hobbies");
            }
            const data: Hobby[] = await response.json();
            hobbies.value = data.sort((a, b) => a.name.localeCompare(b.name));
          } catch (error) {
            console.error("Error fetching hobbies:", error);
          }
        };
  
        const fetchAllHobbies = async () => {
          try {
            const response = await fetch("/api/all-hobbies/");
            if (!response.ok) {
              throw new Error("Failed to fetch all hobbies");
            }
            const data: Hobby[] = await response.json();
            allHobbies.value = data;
          } catch (error) {
            console.error("Error fetching all hobbies:", error);
          }
        };
  
        function getCsrfToken(): string {
          const match = document.cookie.match(/csrftoken=([^;]+)/);
          return match ? match[1] : '';
        }
  
        const addHobby = async () => {
          let hobbyId = selectedHobbyId.value;

          const existingHobby = hobbies.value.find(
            (hobby) => hobby.id === Number(hobbyId) || hobby.name === newHobbyName.value
          );

          if (existingHobby) {
            Message.value = `You already have the hobby "${existingHobby.name}"!`;
            setTimeout(() => {
              Message.value = null;
            }, 5000);
            return;
          }
  
          if (hobbyId === "other" && newHobbyName.value) {
            try {
              const response = await fetch("/api/hobbies/create/", {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ name: newHobbyName.value }),
              });
  
              if (!response.ok) {
                throw new Error("Failed to create new hobby");
              }
  
              const newHobby: Hobby = await response.json();
              allHobbies.value.push(newHobby);
              selectedHobbyId.value = newHobby.id.toString();
  
              const addUserHobbyResponse = await fetch("/api/hobbies/add/", {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ hobby_id: newHobby.id }),
              });
  
              if (!addUserHobbyResponse.ok) {
                throw new Error("Failed to add hobby to user");
              }
  
              fetchHobbies();
              selectedHobbyId.value = "";
              newHobbyName.value = "";
  
              Message.value = "Hobby has been added!";
              setTimeout(() => {
                Message.value = null;
              }, 5000);
            } catch (error) {
              console.error("Error adding hobby:", error);
            }
          } else {
            try {
              const response = await fetch("/api/hobbies/add/", {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ hobby_id: hobbyId }),
              });
  
              if (!response.ok) {
                throw new Error("Failed to add hobby to user");
              }
  
              fetchHobbies();
              selectedHobbyId.value = "";
  
              Message.value = "Hobby has been added!";
              setTimeout(() => {
                Message.value = null;
              }, 5000);
            } catch (error) {
              console.error("Error adding hobby:", error);
            }
          }
        };
  
        const confirmDelete = (hobby: Hobby) => {
          const userConfirmed = window.confirm(`Are you sure you want to delete the hobby "${hobby.name}"?`);
          if (userConfirmed) {
            deleteHobby(hobby.id);
          }
        };
  
        const deleteHobby = async (hobbyId: number) => {
          try {
            const csrfToken = getCsrfToken();
            const response = await fetch(`/api/hobbies/${hobbyId}/`, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
              },
            });
  
            if (!response.ok) {
              throw new Error("Failed to delete hobby");
            }
  
            hobbies.value = hobbies.value.filter(hobby => hobby.id !== hobbyId);
          } catch (error) {
            console.error("Error deleting hobby:", error);
          }
        };
  
        onMounted(() => {
          fetchHobbies();
          fetchAllHobbies();
        });
  
        return { hobbies, allHobbies, selectedHobbyId, newHobbyName, Message, addHobby, deleteHobby, confirmDelete };
      },
    });
</script>
  
<style scoped>
  /* Define color variables for reuse and easy theme adjustments */
  :root {
    --color-bg: #def2f1;
    --color-text-primary: #17252a;
    --color-text-secondary: #2b7a78;
    --color-text-light: #feffff;
    --color-button-bg: #3aafa9;
    --color-button-hover: #2b7a78;
    --color-border: #2b7a78;
    --color-accent: #3aafa9;
  }

  .hobbies-list {
    background-color: var(--color-bg);
    color: var(--color-text-primary);
    min-height: 600px;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  /* Typography classes using consistent values */
  .text-17252A {
    color: var(--color-text-primary);
    font-weight: 600;
  }

  .text-feffff {
    color: var(--color-text-light);
  }

  .text-2b7a78 {
    color: var(--color-text-secondary);
  }

  .bg-def2f1 {
    background-color: var(--color-bg);
  }

  .btn-3aafa9 {
    background-color: var(--color-button-bg);
    border: 1px solid var(--color-button-bg);
    color: var(--color-text-light);
    transition: background-color 0.3s, border-color 0.3s;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
  }

  .btn-3aafa9:hover {
    background-color: var(--color-button-hover);
    border-color: var(--color-button-hover);
  }

  .border-2b7a78 {
    border-color: var(--color-border);
  }

  .alert {
    font-size: 0.9rem;
    padding: 10px;
    border-radius: 4px;
    background-color: #f8d7da; /* subtle error background */
    color: #721c24; /* error text color */
    margin-top: 10px;
  }

  .list-group-item {
    border: 1px solid var(--color-border);
    border-radius: 0;
    background-color: var(--color-bg);
    color: var(--color-text-primary);
    padding: 10px 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 0.5rem;
  }

  .list-group-item:first-of-type {
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }

  .list-group-item:last-of-type {
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  }

  .list-group-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }

  h2 {
    font-size: 1.5rem;
    color: var(--color-text-primary);
    border-bottom: 2px solid var(--color-accent);
    padding-bottom: 5px;
    margin-bottom: 1rem;
  }

  /* Responsive adjustments for smaller screens */
  @media (max-width: 600px) {
    .hobbies-list {
      padding: 15px;
    }

    .btn-3aafa9 {
      width: 100%;
      padding: 0.75rem;
    }

    .list-group-item {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>

  