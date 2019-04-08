<template>
  <div>
    <header>
      <h1>{{ title }}</h1>
    </header>
    <ul>
      <li v-for="prog in programmers" v-on:click="prog.show=!prog.show" :key="prog">
        <h2>{{ prog.name }}</h2>
        <h3>{{ prog.speciality }}</h3>
        <h4 v-show="prog.show">{{ prog.email }}</h4>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data () {
    return{
      title: 'The Programmers',
      programmers:[
        {name:'Almog', speciality:'Front End',email:'almoggr@ac.sce.ac.il',show:false},
        {name:'Shmoel',speciality:'Front End',email:'shmuemo1@ac.sce.ac.il',show:false},
        {name:'Alex',speciality:'Back End',email:'alexwe@ac.sce.ac.il',show:false},
        {name:'Mishel',speciality:'Back End',email:'misheel@ac.sce.ac.il',show:false}
      ]
    }
  },
}
</script>

<style scoped>
#programmers{
  width:100%;
  max-width:1200px;
  margin:40px auto;
  padding:0 20px;
  box-sizing:border-box;
}
ul{
  display: flex;
  flex-wrap: wrap;
  list-style-type: none;
  padding: 0;
}
li{
  flex-grow: 1;
  flex-basis: 300px;
  text-align: center;
  padding: 100px;
  border: 1px solid #222;
  margin: 10px;
}
header{
  background: lightgreen;
  padding:  10px;
}
h1{
  color: #222;
  text-align: center;
}
</style>
