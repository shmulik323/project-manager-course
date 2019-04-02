<template>
  <div id="search">
  <h1> Search <h1>
  <p>{{ search() }}<p>

  </div>
</template>
<script>
export default {
    data(){
        return {
            title: 'your first vue'
        }
    },
    methods: {
        search: function(){
            return 'have';
        }
    },
}
</script>

