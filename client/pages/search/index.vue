<template>
  <div id="search">
    <h1>Search</h1>
    <p>{{ title }}</p>
  </div>
</template>
<script>
export default {
  data() {
    return {
      title: "wip(Work in progress)"
    };
  },
  methods: {
    search: function() {
      return "have";
    }
  }
};
</script>

