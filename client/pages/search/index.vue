<template>
  <v-card id="search">
    <v-card-title>
      <v-text-field v-model="searchText" append-icon="search" label="Search" hide-details></v-text-field>
    </v-card-title>
    <div>
      <v-btn @click="search()">get patents</v-btn>
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
      this.$router.push(`search/result/${this.searchText}`);
    }
  }
};
</script>

