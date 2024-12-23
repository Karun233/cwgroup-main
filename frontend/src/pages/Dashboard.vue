<template>
    <div class="mt-4">
      <h3>Hello {{ userName }}</h3>
    </div>
  
    <div class="row mt-5">
      <div class="col-md-4">
        <div class="box p-4 text-white bg-info rounded-lg shadow-lg">
          <h4>Friend Requests</h4>
        </div>
      </div>
  
      <div class="col-md-4">
        <div class="box p-4 text-white bg-teal rounded-lg shadow-lg">
          <h4>Friends</h4>
        </div>
      </div>
  
      <div class="col-md-4">
        <div class="box p-4 text-white bg-lightTeal rounded-lg shadow-lg">
          <h4>Pending Requests</h4>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  
  interface User {
    name: string;
  }
  
  export default defineComponent({
    name: 'Dashboard',
    setup() {
      const userName = ref<string>('');
  
      const fetchUsername = async (): Promise<void> => {
        try {
          const response = await fetch('/api/profile', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
  
          if (response.ok) {
            const data: User = await response.json(); 
            userName.value = data.name;
          } else {
            console.error('Failed to fetch username:', response.status);
            userName.value = ''; 
          }
        } catch (error) {
          console.error('Error fetching username:', error);
          userName.value = '';
        }
      };
  
      onMounted(() => {
        fetchUsername();
      });
  
      return { userName };
    },
  });
  </script>
  
  <style scoped>
  .bg-main {
    background-color: #2b7a78;
  }
  
  .bg-info {
    background-color: #3aafa9 !important;
  }
  
  .bg-teal {
    background-color: #3aafa9 !important;
  }
  
  .bg-lightTeal {
    background-color: #3aafa9 !important;
  }
  
  .text-danger {
    color: #feffff !important;
  }
  
  .box {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
  }
  
  .box:hover {
    transform: translateY(-5px);
  }
  
  .nav-link {
    font-weight: bold;
    color: #feffff !important;
    text-transform: uppercase;
  }
  
  .nav-link:hover {
    text-decoration: underline;
  }
  
  h2 {
    font-size: 2rem;
    font-weight: bold;
    color: #feffff;
  }
  
  h3 {
    font-size: 3rem;
    font-weight: 500;
    color: #17252A;
  }
  
  @media (max-width: 768px) {
    .box {
      margin-bottom: 20px;
    }
  }
  </style>