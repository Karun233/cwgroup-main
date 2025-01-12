import { defineStore } from "pinia";

interface Profile {
  username: string;
  name: string;
  email: string;
  date_of_birth: string;
}

interface FriendRequest {
  id: number;
  sender: {
    id: number;
    username: string;
  };
}

interface Friend {
  id: number;
  username: string;
}

interface UserState {
  // Basic user data
  profile: Profile;
  userName: string;

  // For searching other users
  searchQuery: string;
  foundUsers: { id: number; username: string }[];

  // Friends data
  friendRequests: FriendRequest[];
  friends: Friend[];

  // If you want to track total users, pending requests, etc. add them here
}

const getCsrfToken = (): string | null => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

export const useUserStore = defineStore("user", {
  state: (): UserState => ({
    profile: {
      username: "",
      name: "",
      email: "",
      date_of_birth: "",
    },
    userName: "",

    searchQuery: "",
    foundUsers: [],

    friendRequests: [],
    friends: [],
  }),

  actions: {
    // ---------------------
    // Fetch Profile (GET)
    // ---------------------
    async fetchProfile(): Promise<void> {
      try {
        const response = await fetch(`/api/profile`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch profile. Status: ${response.status}`);
        }
        const data = await response.json();
        // Update local state
        this.profile = data;
        this.userName = data.name || ""; // For display on dashboard
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },

    // ---------------------
    // Update Profile (POST)
    // ---------------------
    async updateProfile(): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/api/profile`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
          body: JSON.stringify(this.profile),
        });
        if (!response.ok) {
          console.error("Failed to update profile");
        } else {
          // Optionally re-fetch to ensure up-to-date state
          await this.fetchProfile();
          alert("Profile updated successfully");
        }
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },

    // ---------------------
    // Find Users (GET)
    // ---------------------
    async findUsers(): Promise<void> {
      try {
        const response = await fetch(`/api/users?search=${this.searchQuery}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch users");
        }
        this.foundUsers = await response.json();
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },

    // ---------------------
    // Friend Requests
    // ---------------------
    async fetchFriendRequests(): Promise<void> {
      try {
        const response = await fetch(`/api/friend-requests/`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch friend requests");
        }
        this.friendRequests = await response.json();
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    },

    // Send Friend Request
    async sendFriendRequest(receiverId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/api/friend-request/send/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
          body: JSON.stringify({ receiver_id: receiverId }),
        });
        if (!response.ok) {
          throw new Error("Failed to send friend request");
        }
        alert("Friend request sent!");
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    },

    // Accept Friend Request
    async acceptFriendRequest(requestId: number): Promise<void> {
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
          throw new Error("Failed to accept friend request");
        }
        alert("Friend request accepted!");
        // Refresh friend requests/friends list
        this.fetchFriendRequests();
        this.fetchFriends();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    },

    // Decline Friend Request
    async declineFriendRequest(requestId: number): Promise<void> {
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
          throw new Error("Failed to decline friend request");
        }
        alert("Friend request declined!");
        this.fetchFriendRequests();
      } catch (error) {
        console.error("Error declining friend request:", error);
      }
    },

    // ---------------------
    // Fetch Friends
    // ---------------------
    async fetchFriends(): Promise<void> {
      try {
        const response = await fetch(`/api/friends/`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch friends");
        }
        this.friends = await response.json();
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    },
  },
});
