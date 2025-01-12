import { defineStore } from "pinia";

interface Hobby {
  id: number;
  name: string;
}

interface HobbyState {
  hobbies: Hobby[];
  allHobbies: Hobby[];

  selectedHobbyId: string;
  newHobbyName: string;
  message: string | null;
}

const getCsrfToken = (): string | null => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

export const useHobbyStore = defineStore("hobbies", {
  state: (): HobbyState => ({
    hobbies: [],
    allHobbies: [],
    selectedHobbyId: "",
    newHobbyName: "",
    message: null,
  }),

  actions: {
    // Fetch user’s current hobbies
    async fetchHobbies(): Promise<void> {
      try {
        const response = await fetch(`/api/hobbies/`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch hobbies: ${response.status}`);
        }
        const data: Hobby[] = await response.json();
        // Sort them if desired
        this.hobbies = data.sort((a, b) => a.name.localeCompare(b.name));
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },

    // Fetch all possible hobbies
    async fetchAllHobbies(): Promise<void> {
      try {
        const response = await fetch(`/api/all-hobbies/`, {
          method: "GET",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch all hobbies");
        }
        const data: Hobby[] = await response.json();
        this.allHobbies = data;
      } catch (error) {
        console.error("Error fetching all hobbies:", error);
      }
    },

    // Add a new or existing hobby
    async addHobby(): Promise<void> {
      if (!this.selectedHobbyId) return;

      // Duplicate check
      const existing = this.hobbies.find(
        (h) =>
          h.id === Number(this.selectedHobbyId) ||
          h.name.toLowerCase() === this.newHobbyName.toLowerCase()
      );
      if (existing) {
        this.message = `You already have the hobby "${existing.name}"!`;
        setTimeout(() => (this.message = null), 3000);
        return;
      }

      const csrfToken = getCsrfToken();
      try {
        if (this.selectedHobbyId === "other" && this.newHobbyName) {
          // 1) Create new hobby
          const createResp = await fetch(`/api/hobbies/create/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken || "",
            },
            credentials: "include",
            body: JSON.stringify({ name: this.newHobbyName }),
          });

          if (!createResp.ok) {
            throw new Error("Failed to create new hobby");
          }
          const newHobby: Hobby = await createResp.json();
          this.allHobbies.push(newHobby);

          // 2) Add that hobby to the user
          const addUserResp = await fetch(`/api/hobbies/add/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken || "",
            },
            credentials: "include",
            body: JSON.stringify({ hobby_id: newHobby.id }),
          });
          if (!addUserResp.ok) {
            throw new Error("Failed to add hobby to user");
          }

          await this.fetchHobbies();

          this.selectedHobbyId = "";
          this.newHobbyName = "";
          this.message = "New hobby added!";
          setTimeout(() => (this.message = null), 3000);
        } else {
          // Existing hobby
          const addResp = await fetch(`/api/hobbies/add/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken || "",
            },
            credentials: "include",
            body: JSON.stringify({ hobby_id: Number(this.selectedHobbyId) }),
          });
          if (!addResp.ok) {
            throw new Error("Failed to add hobby to user");
          }
          await this.fetchHobbies();
          this.selectedHobbyId = "";
          this.newHobbyName = "";
          this.message = "Hobby has been added!";
          setTimeout(() => (this.message = null), 3000);
        }
      } catch (error) {
        console.error("Error adding hobby:", error);
      }
    },

    // Delete a hobby from the user’s list
    async deleteHobby(hobbyId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const resp = await fetch(`/api/hobbies/${hobbyId}/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
        });
        if (!resp.ok) {
          throw new Error("Failed to delete hobby");
        }
        // Immediately remove it from the local array
        this.hobbies = this.hobbies.filter((h) => h.id !== hobbyId);
      } catch (error) {
        console.error("Error deleting hobby:", error);
      }
    },

    confirmDelete(hobbyId: number, hobbyName: string) {
      const userConfirmed = window.confirm(
        `Are you sure you want to delete the hobby "${hobbyName}"?`
      );
      if (userConfirmed) {
        this.deleteHobby(hobbyId);
      }
    },
  },
});
