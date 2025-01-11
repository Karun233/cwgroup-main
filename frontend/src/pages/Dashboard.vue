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
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "Dashboard",
  setup() {
    const userName = ref<string>("");
    const searchQuery = ref<string>("");
    const foundUsers = ref<any[]>([]);
    const friendRequests = ref<any[]>([]);
    const friends = ref<any[]>([]);

    const getCsrfToken = (): string | null => {
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      return match ? match[1] : null;
    };

    // Fetch the logged-in user's name
    const fetchUsername = async () => {
      const response = await fetch("/api/profile", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      const data = await response.json();
      userName.value = data.name || "";
    };

    // Search for users
    const findUsers = async () => {
      try {
        const response = await fetch(`/api/users?search=${searchQuery.value}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch users");
        }
        foundUsers.value = await response.json();
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    // Send a friend request
    const sendFriendRequest = async (receiverId: number): Promise<void> => {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch("/api/friend-request/send/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
          body: JSON.stringify({ receiver_id: receiverId }),
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        alert("Friend request sent!");
        console.log("Friend request sent successfully");
      } catch (error) {
        console.error("Error sending friend request:", error);
        alert("Could not send friend request: " + error);
      }
    };

    // Fetch friend requests for logged-in user
    const fetchFriendRequests = async () => {
      try {
        const response = await fetch("/api/friend-requests/", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch friend requests");
        }
        friendRequests.value = await response.json();
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    };

    // Accept a friend request
    const acceptFriendRequest = async (requestId: number) => {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/api/friend-request/manage/${requestId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
          body: JSON.stringify({ action: "accept" }),
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        alert("Friend request accepted!");
        // Refresh friend requests and friend list
        fetchFriendRequests();
        fetchFriends();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    // Decline a friend request
    const declineFriendRequest = async (requestId: number) => {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/api/friend-request/manage/${requestId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
          body: JSON.stringify({ action: "decline" }),
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        alert("Friend request declined!");
        // Refresh friend requests
        fetchFriendRequests();
      } catch (error) {
        console.error("Error declining friend request:", error);
      }
    };

    // Fetch the logged-in user's friends
    const fetchFriends = async () => {
      try {
        const response = await fetch("/api/friends/", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch friends");
        }
        friends.value = await response.json();
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    };

    // Lifecycle Hook
    onMounted(() => {
      fetchUsername();
      fetchFriendRequests();
      fetchFriends();
    });

    return {
      userName,
      searchQuery,
      foundUsers,
      friendRequests,
      friends,
      findUsers,
      sendFriendRequest,
      acceptFriendRequest,
      declineFriendRequest,
    };
  },
});
</script>
