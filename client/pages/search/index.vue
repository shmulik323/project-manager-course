<template>
  <v-card id="search">
    <v-card-media
      height="350px"
      aspect-ratio="0.5"
      lazy-src="https://image.freepik.com/free-photo/colorful-letters-forming-word-copyright_53876-31425.jpg"
    ></v-card-media>
    <v-card-title>
      <v-text-field id="name" v-model="searchText" append-icon="search" label="Search" hide-details></v-text-field>
    </v-card-title>
    <div>
      <v-btn id="search" @click="search()">Search</v-btn>
    </div>
  </v-card>
</template>
<script>
export default {
  data() {
    return {
      pData: "",
      searchText: "",
      applicationType: ""
    };
  },
  methods: {
    search: function() {
      this.$router.push(`/search/result/${this.searchText}`);
    }
  }
};
</script>

