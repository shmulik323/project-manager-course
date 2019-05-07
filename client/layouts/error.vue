<template functional>
  <div class="row">
    <div class="col-md-12">
      <div class="error-template">
        <h1>Oops!</h1>
        <h2>404 Not Found</h2>
        <div class="error-details">Sorry, an error has occured, Requested page not found!</div>
        <div class="error-actions">
          <nuxt-link class="btn btn-primary btn-lg" to="/">
            <span class="glyphicon glyphicon-home"></span>
            Take Me Home
          </nuxt-link>
          <nuxt-link class="btn btn-default btn-lg" to="/contact">
            <span class="glyphicon glyphicon-envelope"></span> Contact Support
          </nuxt-link>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.error-template {
  padding: 40px 15px;
  text-align: center;
}
.error-actions {
  margin-top: 15px;
  margin-bottom: 15px;
}
.error-actions .btn {
  margin-right: 10px;
}
</style>
