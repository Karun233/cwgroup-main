<template>
  <main class="container py-5">
      <div class="d-flex justify-content-between align-items-center bg-main text-light p-4 rounded-lg shadow-lg mb-4">
        <router-link to="/dashboard" class="h2 m-0 text-decoration-none text-light">Dashboard</router-link>
        <nav>
          <ul class="nav">
            <li class="nav-item">
              <router-link to="/profile" class="nav-link text-light">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/hobbies" class="nav-link text-light">Hobbies</router-link>
            </li>
            <li class="nav-item">
              <a href="/logout" class="nav-link text-light">Logout</a>
            </li>
          </ul>
        </nav>
      </div>
      <RouterView class="flex-shrink-0" />
  </main>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
  components: { RouterView },
});

</script>

<style scoped>
.bg-main {
  background-color: #0b9ebb;

}

.nav-link {
  font-weight: bold;
  text-transform: uppercase;
  transition: color 0.3s ease-in-out;
}

.nav-link:hover {
  text-decoration: underline;
}

/* .router-link-active {
  font-weight: bold;
  color: #fff; 
} */


</style>