<template>
  <div>
    <h3>Hello {{ userName }}</h3>

    <!-- Send Friend Request -->
    <div class="send-friend">
      <input v-model="searchQuery" placeholder="Search for a user" class="form-control" />
      <button @click="findUsers" class="btn btn-primary mt-2">Search</button>
      <ul v-if="foundUsers.length > 0" class="list-group mt-2">
        <li
          v-for="user in foundUsers"
          :key="user.id"
          class="list-group-item d-flex justify-content-between"
        >
          {{ user.username }}
          <button @click="sendFriendRequest(user.id)" class="btn btn-success btn-sm">
            Send Request
          </button>
        </li>
      </ul>
    </div>

    <!-- Friend Requests -->
    <div class="friend-requests mt-4">
      <h4>Friend Requests</h4>
      <ul v-if="friendRequests.length > 0" class="list-group">
        <li
          v-for="request in friendRequests"
          :key="request.id"
          class="list-group-item d-flex justify-content-between"
        >
          {{ request.sender.username }}
          <div>
            <button @click="acceptFriendRequest(request.id)" class="btn btn-primary btn-sm">
              Accept
            </button>
            <button @click="declineFriendRequest(request.id)" class="btn btn-danger btn-sm">
              Decline
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Friends List -->
    <div class="friends-list mt-4">
      <h4>My Friends</h4>
      <ul v-if="friends.length > 0" class="list-group">
        <li v-for="friend in friends" :key="friend.id" class="list-group-item">
          {{ friend.username }}
        </li>
      </ul>
      <p v-else>No friends yet.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { storeToRefs } from "pinia";               // <-- import storeToRefs
import { useUserStore } from "../stores/useUserStore";

export default defineComponent({
  name: "Dashboard",
  setup() {
    const userStore = useUserStore();

    // Use storeToRefs to convert store state to reactive refs
    const {
      userName,
      searchQuery,
      foundUsers,
      friendRequests,
      friends
    } = storeToRefs(userStore);

    // Lifecycle Hook
    onMounted(() => {
      userStore.fetchProfile();
      userStore.fetchFriendRequests();
      userStore.fetchFriends();
    });

    return {
      // State (all are now refs)
      userName,
      searchQuery,
      foundUsers,
      friendRequests,
      friends,

      // Actions (we can reference them directly from userStore)
      findUsers: userStore.findUsers,
      sendFriendRequest: userStore.sendFriendRequest,
      acceptFriendRequest: userStore.acceptFriendRequest,
      declineFriendRequest: userStore.declineFriendRequest,
    };
  },
});
</script>
